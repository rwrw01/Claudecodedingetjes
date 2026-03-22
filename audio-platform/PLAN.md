# Audio-opnameplatform voor Digitaal Vakmanschap

## Context
We bouwen een webplatform waar uitgenodigde deelnemers hun gedachten over "digitaal vakmanschap" kunnen inspreken via audio-opnames. De opnames worden getranscribeerd (Mistral Voxtral API) en samengevat. Het platform moet stabiel werken op mobiel en desktop, met speciale aandacht voor Bluetooth-microfoonafhandeling.

**Deployment**: Als Docker container in de bestaande [sovereign-stack](https://github.com/rwrw01/sovereign-stack) op Hetzner VPS, achter Traefik reverse proxy, met sovereign-elite hardening standaarden.

## Architectuur

### Sovereign-stack integratie
- **Docker container** met hardening: `no-new-privileges`, `cap_drop: ALL`, `read_only: true`, memory/PID limits
- **Traefik** voor TLS-terminatie en routing (bijv. `audio.jouwdomein.nl`)
- **Keycloak** voor admin dashboard authenticatie (OIDC/SSO)
- **PostgreSQL 16** (bestaande instance) in plaats van SQLite — past bij de stack
- **CrowdSec** bescherming via bestaande bouncers
- **Eigen Docker network** (geïsoleerd, zero-trust)
- Audio-bestanden op gemounte volume met `noexec,nosuid,nodev`
- **Database-encryptie**: PostgreSQL SSL/TLS connectie verplicht (`sslmode=require`), gevoelige velden (email, naam) versleuteld met AES-256-GCM in de applicatielaag, encryptie-sleutel via environment variable
- **Audio-encryptie**: bestanden at-rest versleuteld via AES-256 voordat ze naar disk geschreven worden, ontsleuteld bij transcriptie/afspelen

### Tech stack
- **Node.js 22 + Express** — backend
- **PostgreSQL 16** — database (via bestaande sovereign-stack instance, SSL verplicht)
- **Pure HTML/CSS/JS** — frontend (geen frameworks, past bij bestaand project)
- **Mistral Voxtral API** (`voxtral-mini-2602`) — transcriptie (Nederlands, $0.003/min)
- **Mistral LLM API** — samenvatting
- **Nodemailer** — magic link e-mails
- **AES-256-GCM** — applicatie-niveau encryptie voor PII en audio bestanden

## Bestandsstructuur

```
audio-platform/
├── Dockerfile
├── docker-compose.yml          # Standalone + sovereign-stack integratie
├── package.json
├── .env.example
├── server.js                   # Express server
├── src/
│   ├── db.js                   # PostgreSQL connectie + schema
│   ├── routes/
│   │   ├── invitations.js      # Magic link CRUD + validatie
│   │   ├── recordings.js       # Audio upload + opslag
│   │   ├── transcription.js    # Mistral Voxtral API
│   │   └── admin.js            # Admin dashboard API
│   ├── middleware/
│   │   ├── auth.js             # Magic link token validatie
│   │   └── adminAuth.js        # Keycloak OIDC verificatie
│   └── services/
│       ├── mistral.js          # Voxtral transcriptie + samenvatting
│       └── mailer.js           # E-mail verzending
├── public/
│   ├── record.html             # Opnamepagina (hoofdpagina voor deelnemers)
│   ├── record.css
│   ├── record.js               # Audio-opname logica
│   └── admin.html              # Admin dashboard
├── uploads/                    # Audio bestanden (Docker volume)
└── tests/
    └── api.test.js
```

## Database schema (PostgreSQL)

```sql
CREATE TABLE invitations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token VARCHAR(64) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    used_at TIMESTAMPTZ,
    max_recordings INT DEFAULT 3
);

CREATE TABLE recordings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invitation_id UUID REFERENCES invitations(id),
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(512) NOT NULL,
    duration_seconds FLOAT,
    file_size_bytes BIGINT,
    mime_type VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE transcriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID REFERENCES recordings(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'nl',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID REFERENCES recordings(id) ON DELETE CASCADE,
    summary TEXT NOT NULL,
    key_topics TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Implementatieplan

### Stap 1: Project setup
- `package.json` met dependencies: express, pg, multer, nodemailer, node-fetch
- `src/crypto.js` — AES-256-GCM encryptie/decryptie module voor database velden en audio bestanden
- `.env.example` met benodigde variabelen
- `Dockerfile` (Node.js 22 Alpine, non-root user)
- `docker-compose.yml` met sovereign-stack hardening

### Stap 2: Database en server
- `src/db.js` — PostgreSQL pool + auto-migratie (schema aanmaken bij start)
- `server.js` — Express app met routes, static files, error handling
- Rate limiting en basis security headers (helmet)

### Stap 3: Magic link systeem
- `POST /api/invitations` — genereer uitnodiging (admin)
- `GET /api/invitations/:token/validate` — valideer token
- `GET /record?token=xxx` — redirect naar opnamepagina
- Token: 32 bytes crypto.randomBytes, URL-safe base64
- Vervaltijd: 30 dagen standaard
- E-mail verzending via SMTP (Nodemailer)

### Stap 4: Frontend opnamepagina (PRIORITEIT)
Dit is het kernstuk. Speciale aandacht voor microfoon-stabiliteit:

**Microfoon-afhandeling:**
- `navigator.mediaDevices.enumerateDevices()` voor apparaatlijst
- Dropdown met alle beschikbare microfoons (label + id)
- Default: systeemstandaard, maar gebruiker kan wisselen
- `devicechange` event listener voor Bluetooth connect/disconnect
- Bij device-wissel: automatisch stream herstarten
- Foutafhandeling: als geselecteerd apparaat verdwijnt, waarschuwing tonen

**Audio-opname:**
- MediaRecorder API met `audio/webm;codecs=opus` (fallback: `audio/mp4`)
- Real-time geluidsniveau meter via AnalyserNode (zodat je ZIET dat de juiste mic actief is)
- Opnametimer (mm:ss)
- Start/stop/pauze knoppen
- Na opname: terugluisteren voor je indient
- Maximum opnameduur: 10 minuten
- Chunk-gebaseerd opnemen (elke 1s een chunk) voor stabiliteit

**UX-flow:**
1. Token validatie → welkomstscherm met uitleg
2. Microfoon toestemming vragen → apparaat selectie
3. Geluidsniveau-test ("Zeg iets om je microfoon te testen")
4. Opname starten → timer + niveau-meter
5. Opname stoppen → terugluisteren
6. Tevreden? → Uploaden met voortgangsbalk
7. Bedankpagina

**Styling:** Aansluitend bij bestaand project (Segoe UI, #2563eb primary, cards met schaduw, 12px radius)

### Stap 5: Audio upload en opslag
- `POST /api/recordings` — upload audio (multer, max 50MB)
- Opslaan in `uploads/` directory (Docker volume)
- Bestandsnaam: `{uuid}.webm`
- Na succesvolle upload: automatisch transcriptie starten (async)

### Stap 6: Transcriptie (Mistral Voxtral)
- `POST https://api.mistral.ai/v1/audio/transcriptions`
- Model: `voxtral-mini-2602`
- Ondersteunt: .webm, .mp3, .wav, .m4a, .ogg (max 1GB)
- Nederlands wordt ondersteund
- Resultaat opslaan in transcriptions tabel
- Na transcriptie: automatisch samenvatting genereren

### Stap 7: Samenvatting (Mistral LLM)
- Gebruik Mistral chat API voor samenvatting van transcriptie
- Prompt: "Vat de volgende transcriptie samen over digitaal vakmanschap. Geef een korte samenvatting en de belangrijkste onderwerpen."
- Opslaan in summaries tabel

### Stap 8: Admin dashboard
- Beschermd via Keycloak OIDC (of eenvoudige API key voor eerste versie)
- Overzicht: alle uitnodigingen, opnames, transcripties, samenvattingen
- Uitnodigingen aanmaken en kopiëren
- Opnames beluisteren
- Transcripties en samenvattingen lezen
- Export mogelijkheid (CSV/JSON)

## Container hardening (sovereign-stack standaard)

```yaml
security_opt:
  - no-new-privileges:true
cap_drop:
  - ALL
read_only: true
tmpfs:
  - /tmp:noexec,nosuid,nodev,size=100M
mem_limit: 512m
pids_limit: 100
healthcheck:
  test: ["CMD", "node", "-e", "fetch('http://localhost:3000/health')"]
  interval: 30s
  timeout: 5s
  retries: 3
```

## Encryptie-strategie

### Database connectie
- PostgreSQL SSL/TLS verplicht: `sslmode=require` in connectiestring
- Certificaat verificatie indien beschikbaar (`sslmode=verify-full`)

### Applicatie-niveau encryptie (AES-256-GCM)
- **Waarom**: Database-niveau encryptie (pgcrypto/TDE) beschermt niet tegen SQL injection of database dumps. Applicatie-niveau encryptie betekent dat zelfs bij een database-lek de data onleesbaar is.
- **Wat wordt versleuteld**: naam, email (PII velden in invitations tabel), transcriptietekst, samenvattingen
- **Hoe**: AES-256-GCM via Node.js `crypto` module, elke waarde krijgt eigen IV, opgeslagen als `iv:authTag:ciphertext` (base64)
- **Sleutelbeheer**: `ENCRYPTION_KEY` via environment variable (32 bytes hex), nooit in code of database

### Audio bestanden at-rest
- Bestanden worden versleuteld met AES-256-GCM voordat ze naar disk geschreven worden
- Ontsleuteld on-the-fly bij terugluisteren (admin) of bij verzending naar Mistral API
- Sleutel: zelfde `ENCRYPTION_KEY` of aparte `AUDIO_ENCRYPTION_KEY`

## Environment variabelen (.env)

```
# Server
PORT=3000
NODE_ENV=production
BASE_URL=https://audio.jouwdomein.nl

# Database (SSL verplicht)
DATABASE_URL=postgresql://audio:wachtwoord@postgres:5432/audio_platform?sslmode=require

# Encryptie
ENCRYPTION_KEY=64-hex-chars-hier  # 32 bytes = 256 bit

# Mistral API
MISTRAL_API_KEY=your-key-here

# Email (SMTP)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASS=wachtwoord
SMTP_FROM='"Digitaal Vakmanschap" <noreply@example.com>'

# Admin
ADMIN_API_KEY=secure-random-key
```

## Verificatie
1. `docker compose up` — server start zonder fouten
2. Admin: uitnodiging aanmaken → magic link genereren
3. Magic link openen op mobiel → microfoon toestemming → apparaat selectie
4. Opname maken → terugluisteren → uploaden
5. Controleer: audio bestand op disk, record in database
6. Transcriptie verschijnt na ~30 seconden
7. Samenvatting verschijnt na transcriptie
8. Admin dashboard toont alles correct

## Kritieke bestanden
- `public/record.js` — audio-opname logica (meest complexe bestand)
- `src/services/mistral.js` — Voxtral API integratie
- `src/crypto.js` — AES-256-GCM encryptie module
- `server.js` — Express app configuratie
- `docker-compose.yml` — sovereign-stack deployment
- `Dockerfile` — container build

## Deployment notitie
Bouwen en deployen gebeurt in een aparte sessie met SSH-toegang tot de Hetzner VPS. Dit plan dient als blauwdruk voor die implementatie. De audio-platform container wordt toegevoegd aan de bestaande sovereign-stack docker-compose setup.
