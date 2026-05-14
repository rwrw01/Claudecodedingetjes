import { authenticate } from "./auth";
import { checkAndIncrement } from "./rate-limit";
import { streamAnthropic } from "./anthropic";

type Env = {
  RATE_LIMIT: KVNamespace;
  ANTHROPIC_API_KEY: string;
  TOKEN_KSP?: string;
  TOKEN_JSM?: string;
  ALLOWED_ORIGINS: string;
  MODEL: string;
  MAX_OUTPUT_TOKENS: string;
  DAILY_MESSAGE_LIMIT: string;
};

function corsHeaders(origin: string | null, allowed: string[]): Record<string, string> {
  const allow = origin && allowed.includes(origin) ? origin : allowed[0] ?? "*";
  return {
    "access-control-allow-origin": allow,
    "access-control-allow-methods": "POST, OPTIONS",
    "access-control-allow-headers": "content-type",
    "access-control-max-age": "86400",
    "vary": "origin",
  };
}

function json(data: unknown, init: ResponseInit = {}, cors: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(data), {
    ...init,
    headers: { "content-type": "application/json", ...cors, ...(init.headers ?? {}) },
  });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const allowed = env.ALLOWED_ORIGINS.split(",").map((s) => s.trim());
    const cors = corsHeaders(request.headers.get("origin"), allowed);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    if (url.pathname === "/healthz") {
      return json({ ok: true }, {}, cors);
    }

    if (url.pathname !== "/api/chat" || request.method !== "POST") {
      return json({ error: "Niet gevonden" }, { status: 404 }, cors);
    }

    const token = url.searchParams.get("t");
    const auth = authenticate(token, env);
    if (!auth.ok) {
      return json({ error: auth.error }, { status: auth.status }, cors);
    }

    const dailyLimit = parseInt(env.DAILY_MESSAGE_LIMIT, 10);
    const limitCheck = await checkAndIncrement(env.RATE_LIMIT, auth.userId, dailyLimit);
    if (!limitCheck.ok) {
      return json(
        { error: `Daglimiet bereikt (${dailyLimit} berichten). Probeer het morgen opnieuw.` },
        { status: 429 },
        cors,
      );
    }

    let payload: { pageSlug?: string; messages?: unknown } = {};
    try {
      payload = await request.json();
    } catch {
      return json({ error: "Ongeldige JSON body" }, { status: 400 }, cors);
    }

    const pageSlug = typeof payload.pageSlug === "string" ? payload.pageSlug : "";
    const messages = Array.isArray(payload.messages) ? payload.messages : null;
    if (!pageSlug || !messages) {
      return json({ error: "pageSlug en messages verplicht" }, { status: 400 }, cors);
    }

    const trimmedMessages = messages
      .filter((m): m is { role: "user" | "assistant"; content: string } => {
        return typeof m === "object" && m !== null && (m as { role?: string }).role !== undefined && typeof (m as { content?: unknown }).content === "string";
      })
      .slice(-20);

    if (trimmedMessages.length === 0) {
      return json({ error: "Minstens één bericht nodig" }, { status: 400 }, cors);
    }

    const streamResponse = await streamAnthropic({
      apiKey: env.ANTHROPIC_API_KEY,
      model: env.MODEL,
      maxOutputTokens: parseInt(env.MAX_OUTPUT_TOKENS, 10),
      pageSlug,
      messages: trimmedMessages,
    });

    const headers = new Headers(streamResponse.headers);
    for (const [k, v] of Object.entries(cors)) headers.set(k, v);
    headers.set("x-rate-remaining", String(limitCheck.remaining));
    return new Response(streamResponse.body, { status: streamResponse.status, headers });
  },
};
