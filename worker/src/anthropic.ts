import { buildSystemBlocks } from "./prompt";

type AnthropicMessage = { role: "user" | "assistant"; content: string };

export async function streamAnthropic(params: {
  apiKey: string;
  model: string;
  maxOutputTokens: number;
  pageSlug: string;
  messages: AnthropicMessage[];
}): Promise<Response> {
  const systemBlocks = buildSystemBlocks(params.pageSlug);

  const body = {
    model: params.model,
    max_tokens: params.maxOutputTokens,
    stream: true,
    system: systemBlocks,
    messages: params.messages,
  };

  const upstream = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": params.apiKey,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!upstream.ok || !upstream.body) {
    const errText = await upstream.text().catch(() => "");
    return new Response(JSON.stringify({ error: "Anthropic API fout", status: upstream.status, detail: errText.slice(0, 500) }), {
      status: 502,
      headers: { "content-type": "application/json" },
    });
  }

  return new Response(upstream.body, {
    status: 200,
    headers: {
      "content-type": "text/event-stream",
      "cache-control": "no-cache",
      "x-accel-buffering": "no",
    },
  });
}
