# kasper-tutor — Cloudflare Worker

Proxy tussen de statische lespagina's op GitHub Pages en de Anthropic Claude API. Beveiligt de API key, doet auth via magic-link token, rate-limit per leerling per dag, en injecteert de Kasper-systeemprompt server-side.

## Setup (eenmalig)

```sh
npm install
# Maak KV namespace aan
npx wrangler kv:namespace create RATE_LIMIT
npx wrangler kv:namespace create RATE_LIMIT --preview
# Vul de beide id's in in wrangler.toml
# Zet secrets:
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler secret put TOKEN_KSP
npx wrangler secret put TOKEN_JSM
```

## Lokaal draaien

```sh
# Maak .dev.vars met dezelfde keys (gitignored — niet committen)
npm run dev
```

## Deployen

```sh
npm run deploy
```

## API

`POST /api/chat?t=ksp_xxxxxxxx`

Body:
```json
{ "pageSlug": "6.1-raaklijnen-en-toppen", "messages": [{ "role": "user", "content": "hoi" }] }
```

Response: Server-Sent Events stream van Anthropic.

`GET /healthz` — returns `{ "ok": true }`.

## Beveiliging

- API key alleen in Worker env, NOOIT in client.
- Auth via `?t=<token>` — vergelijken met `TOKEN_KSP` / `TOKEN_JSM` env secrets.
- Rate-limit 100 berichten/dag per token via KV (UTC midnight reset).
- Model en `max_tokens` hardcoded in env vars — client kan deze niet overschrijven.
- Systeem-prompt server-side ingespoten — client kan dyslexie-regels niet wegschrijven.
- History naar laatste 20 berichten getrimd voor input-token-cap.

## Token formaat

Maak per leerling een lange random string, prefix met `ksp_` of `jsm_`:

```sh
# Bash/Linux:
echo "ksp_$(openssl rand -hex 20)"
# PowerShell:
"ksp_" + -join ((1..40) | ForEach-Object { '0123456789abcdef'[(Get-Random -Maximum 16)] })
```
