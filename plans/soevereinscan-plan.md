# SaaS Soevereiniteitsscanner — "SoevereinScan"

## Context
Gemeenten willen controleren of hun cloud/SaaS-leveranciers Amerikaanse infrastructuur gebruiken (CLOUD Act risico, Schrems II/III). Momenteel is er geen open-source tool die dit automatisch in kaart brengt. We bouwen een scansite die via Lookyloo, traceroute en ASN-analyse inzichtelijk maakt welke derde partijen en welke jurisdicties betrokken zijn bij een SaaS-dienst.

**Vergelijkbaar met**: [SoevereinProbe](https://soevereinprobe.nl/) — maar dan open source, self-hosted, en dieper (traceroute + ASN + PeeringDB).

**Deployment**: Docker container in de sovereign-stack op Hetzner VPS.

## Hoe het werkt

```
Gebruiker voert SaaS URL in (bijv. "app.leverancier.nl")
         │
         ▼
┌─────────────────────┐
│  1. Lookyloo scan    │ → Capture alle HTTP requests, redirects,
│     (self-hosted)    │   derde-partij domeinen, IPs, cookies
└────────┬────────────┘
         │ lijst van unieke IPs + domeinen
         ▼
┌─────────────────────┐
│  2. IP → ASN lookup  │ → MaxMind GeoLite2 ASN database (lokaal, gratis)
│     (GeoLite2-ASN)   │   geeft: ASN nummer, organisatienaam, land
└────────┬────────────┘
         │ ASN nummers
         ▼
┌─────────────────────┐
│  3. PeeringDB lookup │ → Organisatiedetails per ASN:
│     (gratis API)     │   naam, land, type (hosting/ISP/enterprise)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  4. RIPE Atlas       │ → Netwerkpad naar elke unieke IP (passief)
│     (Europees/NL)    │   elke hop: IP → ASN → land, geen eigen packets
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  5. GeoIP lookup     │ → MaxMind GeoLite2 City/Country
│     (per IP)         │   fysieke locatie van servers
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  6. Rapport genereren           │
│  - % verkeer naar US jurisdictie│
│  - Lijst alle derde partijen    │
│  - Traceroute visualisatie      │
│  - Risiconiveau per domein      │
│  - CLOUD Act blootstelling      │
└─────────────────────────────────┘
```

## Databronnen

| Bron | Wat het levert | Kosten | Hoe |
|------|---------------|--------|-----|
| **Lookyloo** (self-hosted) | Alle HTTP requests, domeinen, IPs, redirects, cookies, third-party resources | Gratis (BSD-3) | Docker container, pylookyloo API |
| **MaxMind GeoLite2 ASN** | IP → ASN nummer + organisatienaam | Gratis (account vereist) | Lokale MMDB database, wekelijks update |
| **MaxMind GeoLite2 Country** | IP → land + continent | Gratis (account vereist) | Lokale MMDB database |
| **PeeringDB** | ASN → organisatie, land, type, peering info | Gratis API (rate limited) | REST API `https://www.peeringdb.com/api/net?asn=X` |
| **RIPE Atlas** (Amsterdam/NL) | Traceroute via probes wereldwijd, passief (geen packets vanaf eigen IP) | Gratis, 100 metingen/dag | REST API `https://atlas.ripe.net/api/v2/` |
| **RDAP/Whois** | Domeinregistratie, eigenaar, land | Gratis | RDAP API (IANA) |

## Jurisdictie-classificatie

```
VS-risico (CLOUD Act):
- ASN eigenaar is Amerikaans bedrijf (check PeeringDB org.country = "US")
- Server staat fysiek in VS (GeoLite2 Country)
- Moederbedrijf is Amerikaans (handmatige mapping voor grote providers):
  - AWS/Azure/GCP → altijd US jurisdictie, ook EU-regio's
  - Cloudflare, Akamai, Fastly → US
  - OVH, Hetzner, Scaleway → EU

EU-veilig:
- ASN eigenaar is EU-bedrijf
- Server staat in EU
- Geen Amerikaans moederbedrijf

Onbekend/handmatig:
- Niet te classificeren → markeer voor handmatige review
```

## Tech stack

- **Python 3.12 + FastAPI** — backend (past bij pylookyloo, maxminddb, PeeringDB)
- **Lookyloo** — self-hosted Docker container (apart van de app)
- **maxminddb** — Python library voor GeoLite2 MMDB lookups
- **RIPE Atlas API** — passieve traceroute (Europees, RIPE NCC Amsterdam)
- **PostgreSQL 16** — resultaten opslaan (bestaande sovereign-stack instance)
- **Pure HTML/CSS/JS** — frontend (consistent met bestaand project)
- **Redis** — cache voor PeeringDB (7 dagen) + scan deduplicatie (48 uur)

## Bestandsstructuur

```
soevereinscan/
├── Dockerfile
├── docker-compose.yml           # App + Lookyloo + GeoLite2 updater
├── requirements.txt
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app
│   ├── config.py                # Settings via environment
│   ├── models.py                # SQLAlchemy/database models
│   ├── routes/
│   │   ├── scan.py              # POST /api/scan — start scan
│   │   ├── results.py           # GET /api/results/:id — haal resultaat op
│   │   └── admin.py             # Admin endpoints
│   ├── services/
│   │   ├── lookyloo_client.py   # pylookyloo wrapper
│   │   ├── geoip.py             # MaxMind GeoLite2 lookups (ASN + Country)
│   │   ├── peeringdb.py         # PeeringDB API client
│   │   ├── ripe_atlas.py        # RIPE Atlas API (passieve traceroute)
│   │   ├── rdap.py              # RDAP/Whois domein lookup
│   │   ├── classifier.py        # Jurisdictie-classificatie logica
│   │   └── reporter.py          # Rapport generatie
│   └── static/
│       ├── index.html           # Scanpagina
│       ├── results.html         # Resultaatpagina met visualisaties
│       ├── style.css
│       └── app.js               # Frontend logica + visualisaties
├── data/
│   └── us_parent_companies.json # Handmatige mapping: provider → moederbedrijf
├── scripts/
│   └── update-geolite2.sh       # Wekelijkse GeoLite2 database update
└── tests/
    ├── test_geoip.py
    ├── test_peeringdb.py
    └── test_classifier.py
```

## Database schema (PostgreSQL)

```sql
CREATE TABLE scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url VARCHAR(2048) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- pending, scanning, analyzing, done, error
    lookyloo_uuid VARCHAR(64),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    summary JSONB  -- overall risk score, stats
);

CREATE TABLE discovered_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID REFERENCES scans(id) ON DELETE CASCADE,
    url VARCHAR(2048) NOT NULL,
    hostname VARCHAR(255) NOT NULL,
    ip_address INET,
    resource_type VARCHAR(50),  -- script, image, stylesheet, xhr, redirect, iframe
    is_third_party BOOLEAN DEFAULT false
);

CREATE TABLE ip_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID REFERENCES scans(id) ON DELETE CASCADE,
    ip_address INET NOT NULL,
    asn INTEGER,
    asn_org VARCHAR(255),
    country_code CHAR(2),
    city VARCHAR(255),
    peeringdb_org_name VARCHAR(255),
    peeringdb_org_country CHAR(2),
    parent_company VARCHAR(255),       -- uit us_parent_companies.json
    parent_company_country CHAR(2),
    jurisdiction VARCHAR(20),          -- us, eu, unknown
    cloud_act_risk BOOLEAN DEFAULT false
);

CREATE TABLE traceroute_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID REFERENCES scans(id) ON DELETE CASCADE,
    target_ip INET NOT NULL,
    hop_number INTEGER,
    hop_ip INET,
    hop_asn INTEGER,
    hop_asn_org VARCHAR(255),
    hop_country CHAR(2),
    rtt_ms FLOAT
);
```

## Implementatieplan

### Stap 1: Project setup + Lookyloo deployment
- `docker-compose.yml` met Lookyloo container + app container
- `requirements.txt`: fastapi, uvicorn, pylookyloo, maxminddb, asyncpg, httpx, redis
- GeoLite2 database download script
- Sovereign-stack container hardening

### Stap 2: GeoIP + PeeringDB services
- `services/geoip.py` — MaxMind GeoLite2 ASN + Country lookup
- `services/peeringdb.py` — PeeringDB API client met Redis cache
- `data/us_parent_companies.json` — handmatige mapping grote providers
- Unittests voor lookups

### Stap 3: Lookyloo integratie
- `services/lookyloo_client.py` — URL indienen, status pollen, resultaten ophalen
- Parse capture tree: extract alle unieke domeinen + IPs
- Classificeer first-party vs third-party resources

### Stap 4: RIPE Atlas traceroute (passief)
- `services/ripe_atlas.py` — RIPE Atlas API v2 client
- Per uniek IP: traceroute meting aanvragen via RIPE Atlas probes
- Resultaat ophalen (async, kan 30-60s duren)
- Elke hop: IP → ASN → land via lokale GeoLite2
- Geen `CAP_NET_RAW` nodig — geen packets vanaf eigen server

### Stap 5: Jurisdictie-classifier
- `services/classifier.py` — combineer alle data:
  1. GeoLite2: IP → ASN + land
  2. PeeringDB: ASN → organisatie + land
  3. us_parent_companies.json: organisatie → moederbedrijf
  4. Traceroute: passeert verkeer door VS?
- Output: per IP/domein een risicoclassificatie (US/EU/Unknown)

### Stap 6: Frontend scanpagina
- URL invoerveld + scan knop
- Voortgangsindicator (scanning → analyzing → done)
- Polling via `/api/results/:id`

### Stap 7: Resultaatpagina + visualisaties
- **Soevereiniteitsmeter**: % verkeer onder US jurisdictie (visuele meter)
- **Wereldkaart**: waar staan de servers (MaxMind coords)
- **Domeinboom**: Lookyloo-achtige tree van wie wie aanroept
- **Traceroute visualisatie**: hop-voor-hop met landen/ASNs
- **Tabel**: alle derde partijen met risicoclassificatie
- **Export**: PDF rapport voor beleidsdocumenten

### Stap 8: Admin + scan history
- Overzicht van alle uitgevoerde scans
- Beheer van us_parent_companies.json mapping
- Rate limiting (voorkom misbruik)

## Container hardening (sovereign-stack standaard)

```yaml
# soevereinscan app
security_opt:
  - no-new-privileges:true
cap_drop:
  - ALL
read_only: true  # geen CAP_NET_RAW nodig dankzij RIPE Atlas
tmpfs:
  - /tmp:noexec,nosuid,nodev,size=200M
mem_limit: 1g
pids_limit: 200

# lookyloo (apart)
# Gebruikt eigen docker-compose config van Lookyloo project
# Alleen toegankelijk via intern Docker network (niet publiek)
```

## Anti-detectie & rate limiting

### Scan deduplicatie (48 uur)
- Zelfde URL binnen 48 uur → cached resultaat teruggeven, geen nieuwe scan
- Redis key: `scan:{sha256(url)}` met 48-uur TTL
- Gebruiker ziet melding: "Deze URL is recent gescand, resultaat van [datum]"

### Lookyloo anti-botdetectie
- Maximaal **1 capture per minuut** (queue met delay)
- Random **User-Agent rotation** uit pool van gangbare browsers
- Random **viewport sizes** (desktop/tablet/mobiel)
- **Accept-Language: nl-NL,nl;q=0.9** — lijkt op Nederlands browserverkeer
- Geen parallelle captures — sequentieel verwerken
- Optioneel: random delay 2-8 seconden tussen navigatieacties

### PeeringDB caching (7 dagen)
- Redis cache per ASN: `peeringdb:asn:{number}` met 7-dagen TTL
- ASN-informatie verandert zelden, 7 dagen is conservatief
- Reduceert API calls met ~95% bij herhaalde scans
- Fallback: als cache miss en API down → markeer als "enrichment pending"

### RIPE Atlas (passief, geen eigen IP-risico)
- Traceroute wordt uitgevoerd door RIPE Atlas probes, niet door onze server
- Geen ICMP/UDP packets vanaf ons IP → geen blokkeerrisico
- 100 gratis metingen per dag (voldoende voor ~10-15 scans/dag met elk ~7 unieke IPs)
- RIPE NCC is Europese stichting, gevestigd in Amsterdam — volledig EU-jurisdictie
- Resultaten gecached: zelfde IP binnen 48 uur → geen nieuwe meting

### MaxMind GeoLite2 (volledig lokaal)
- Database draait lokaal in container — geen externe API calls
- Geen detectierisico, onbeperkte lookups
- Wekelijkse update via cron/script

## Docker-compose overzicht

```yaml
services:
  soevereinscan:
    build: .
    networks:
      - proxy        # Traefik
      - internal     # Lookyloo + PostgreSQL + Redis
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.soevereinscan.rule=Host(`scan.jouwdomein.nl`)"

  lookyloo:
    image: ghcr.io/lookyloo/lookyloo:latest  # → pin op SHA256
    networks:
      - internal     # ALLEEN intern, niet publiek
    # Lookyloo draait alleen voor de app, niet direct bereikbaar
```

## Environment variabelen

```
# Server
PORT=8000
BASE_URL=https://scan.jouwdomein.nl

# Database
DATABASE_URL=postgresql://soevereinscan:wachtwoord@postgres:5432/soevereinscan?sslmode=require

# Redis (cache)
REDIS_URL=redis://redis:6379/2

# Lookyloo
LOOKYLOO_URL=http://lookyloo:5100

# MaxMind
MAXMIND_LICENSE_KEY=your-key-here  # voor GeoLite2 downloads
GEOLITE2_ASN_PATH=/data/GeoLite2-ASN.mmdb
GEOLITE2_COUNTRY_PATH=/data/GeoLite2-Country.mmdb

# PeeringDB (optioneel, voor hogere rate limits)
PEERINGDB_API_KEY=optional-key

# RIPE Atlas (Europees, RIPE NCC Amsterdam)
RIPE_ATLAS_API_KEY=your-key-here  # gratis account op atlas.ripe.net

# Encryptie (voor PII in scans)
ENCRYPTION_KEY=64-hex-chars
```

## PeeringDB en MaxMind — waarom beide nodig

**Ja, beide zijn essentieel:**
- **MaxMind GeoLite2** (gratis, lokaal): snelle IP→ASN+land lookup, geen API calls nodig, wekelijks update
- **PeeringDB** (gratis API): verrijkt ASN met organisatiedetails, type netwerk, en cruciaal: het **land van de organisatie** (niet het land van de server, maar van de eigenaar)
- De combinatie is krachtig: MaxMind zegt "deze server staat in Frankfurt", PeeringDB zegt "maar de eigenaar is een Amerikaans bedrijf"

## Verificatie
1. `docker compose up` — Lookyloo + app starten
2. URL invoeren (bijv. `https://teams.microsoft.com`) → scan start
3. Lookyloo capture verschijnt met alle resources
4. Per IP: ASN + land + organisatie zichtbaar
5. Traceroute toont route door netwerken
6. Soevereiniteitsmeter toont % US-risico
7. Resultaat exporteerbaar als rapport

## Kritieke bestanden
- `app/services/classifier.py` — jurisdictie-classificatie (kernlogica)
- `app/services/lookyloo_client.py` — Lookyloo integratie
- `app/services/geoip.py` — MaxMind lookups
- `app/services/peeringdb.py` — PeeringDB API
- `app/services/ripe_atlas.py` — RIPE Atlas passieve traceroute
- `data/us_parent_companies.json` — handmatige provider mapping
- `app/static/results.html` — resultaat visualisaties

## Bronnen
- [Lookyloo (CIRCL)](https://github.com/Lookyloo/lookyloo) — BSD-3-Clause
- [PyLookyloo API docs](https://pylookyloo.readthedocs.io/en/latest/api_reference.html)
- [MaxMind GeoLite2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data/)
- [PeeringDB API](https://www.peeringdb.com/apidocs/)
- [SoevereinProbe](https://soevereinprobe.nl/) — vergelijkbaar concept (niet open source)
- [nitefood/asn tool](https://github.com/nitefood/asn) — ASN/traceroute CLI
- [Informatiebeveiligingsdienst](https://www.informatiebeveiligingsdienst.nl/risicos-verwerking-persoonsgegevens-door-amerikaanse-partij/) — risico's voor gemeenten
