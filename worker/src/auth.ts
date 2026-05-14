export type AuthResult = { ok: true; userId: string; naam: string } | { ok: false; status: number; error: string };

export function authenticate(token: string | null, env: { TOKEN_KSP?: string; TOKEN_JSM?: string }): AuthResult {
  if (!token) {
    return { ok: false, status: 401, error: "Geen token meegegeven (?t=...)" };
  }
  if (env.TOKEN_KSP && token === env.TOKEN_KSP) {
    return { ok: true, userId: "ksp", naam: "Kasper" };
  }
  if (env.TOKEN_JSM && token === env.TOKEN_JSM) {
    return { ok: true, userId: "jsm", naam: "Jasmijn" };
  }
  return { ok: false, status: 403, error: "Token onbekend" };
}
