export async function checkAndIncrement(
  kv: KVNamespace,
  userId: string,
  dailyLimit: number,
): Promise<{ ok: true; remaining: number } | { ok: false; remaining: 0; resetUtcDate: string }> {
  const today = new Date().toISOString().slice(0, 10);
  const key = `usage:${userId}:${today}`;
  const current = parseInt((await kv.get(key)) ?? "0", 10);

  if (current >= dailyLimit) {
    return { ok: false, remaining: 0, resetUtcDate: today };
  }

  await kv.put(key, String(current + 1), { expirationTtl: 60 * 60 * 36 });
  return { ok: true, remaining: dailyLimit - current - 1 };
}
