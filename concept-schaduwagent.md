# Concept: De Schaduwagent — AI-gestuurd Incidentbeheer

## 1. Probleemstelling

### Huidige situatie
Bij IT-storingen verloopt de diagnose via een inefficient uitvraagproces:

1. **Gebruiker meldt storing** — vaak vaag: "mijn applicatie doet het niet"
2. **Helpdesk stelt vragen** — "Wat zie je op je scherm?", "Welke foutmelding?", "Heb je al herstart?"
3. **Gebruiker beschrijft onnauwkeurig** — technische context ontbreekt
4. **Ticket wordt slecht gecategoriseerd** — want de uitvraag levert onvoldoende informatie op
5. **Escalatie naar specialisten** — die opnieuw moeten uitzoeken wat er aan de hand is

**Kernprobleem:** Er zit een *mens als vertaallaag* tussen het technische probleem en de oplossing. Die vertaallaag introduceert vertraging, informatieverlies en frustratie.

### Impact
- Langere oplostijden (MTTR)
- Verkeerde categorisering in TOPdesk
- Frustratie bij eindgebruikers
- Specialisten besteden tijd aan diagnose i.p.v. oplossing
- Beheersorganisatie heeft geen goed beeld van werkelijke problematiek

---

## 2. De Oplossing: Schaduwagent

### Kernidee
Een AI-agent die **meedraait bij elke storing** en twee dingen tegelijk doet:

```
┌─────────────────────────────────────────────────────────┐
│                    SCHADUWAGENT                          │
│                                                         │
│   ┌──────────────┐              ┌──────────────────┐    │
│   │  OBSERVATIE   │              │   DIAGNOSE &     │    │
│   │  Meekijken    │◄────────────►│   OPLOSSING      │    │
│   │  met gebruiker│   correlatie │   OS/Systeem     │    │
│   └──────┬───────┘              └────────┬─────────┘    │
│          │                               │              │
│          ▼                               ▼              │
│   Ziet wat de                    Inspecteert logs,      │
│   gebruiker ziet                 services, netwerk,     │
│   (scherm, acties,               configuratie, en       │
│   foutmeldingen)                 voert reparaties uit   │
│                                                         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  AUTOMATISCH TICKET │
              │  - Juiste categorie │
              │  - Rijke context    │
              │  - Oplossing/status │
              └─────────────────────┘
```

### Wat maakt dit anders?
- **Geen uitvraag nodig** — de agent *ziet* wat er misgaat
- **Realtime diagnose** — terwijl de gebruiker het probleem ervaart
- **Daadwerkelijke oplossing** — niet alleen een ticket, maar actie
- **Perfecte documentatie** — het ticket schrijft zichzelf met volledige context

---

## 3. Architectuur

### 3.1 Componenten

```
┌─────────────────────────────────────────────────────────────────┐
│                        GEBRUIKER                                │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ Werkstation                                            │     │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │     │
│  │  │ Screen Agent │  │ OS Agent     │  │ Chat Widget  │  │     │
│  │  │ (observatie) │  │ (diagnose)   │  │ (interactie) │  │     │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │     │
│  └─────────┼─────────────────┼─────────────────┼──────────┘     │
└────────────┼─────────────────┼─────────────────┼────────────────┘
             │                 │                 │
             ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SCHADUWAGENT BACKEND                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Orchestrator (LLM)                     │   │
│  │  - Correleert schermbeeld met systeemdata                │   │
│  │  - Bepaalt diagnose en oplossingspad                     │   │
│  │  - Beslist: automatisch oplossen of escaleren            │   │
│  └──────────┬───────────────────────┬───────────────────────┘   │
│             │                       │                           │
│  ┌──────────▼──────────┐  ┌────────▼────────────────────┐      │
│  │   Kennis & Context  │  │   Actie-engine              │      │
│  │  ┌───────────────┐  │  │  - Service herstart         │      │
│  │  │ BlueDolphin   │  │  │  - Config aanpassing        │      │
│  │  │ (IT-landschap)│  │  │  - Cache clearing           │      │
│  │  ├───────────────┤  │  │  - Netwerk reset            │      │
│  │  │ GGM           │  │  │  - Rechten herstellen       │      │
│  │  │ (Gegevens-    │  │  │  - Scripted remediation     │      │
│  │  │  model)       │  │  └─────────────────────────────┘      │
│  │  ├───────────────┤  │                                        │
│  │  │ Kennisbank    │  │                                        │
│  │  │ (bekende      │  │                                        │
│  │  │  storingen)   │  │                                        │
│  │  └───────────────┘  │                                        │
│  └─────────────────────┘                                        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │   Integraties                                            │   │
│  │  ┌──────────┐ ┌──────────────┐ ┌───────────────────┐    │   │
│  │  │ TOPdesk  │ │ BlueDolphin  │ │ Monitoring        │    │   │
│  │  │ API      │ │ API          │ │ (Zabbix/PRTG/etc) │    │   │
│  │  └──────────┘ └──────────────┘ └───────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Component Details

#### A. Screen Agent (Observatie)
**Doel:** Zien wat de gebruiker ziet — foutmeldingen, applicatiestatus, workflow.

**Aanpak:**
- Periodieke screenshots bij detectie van foutmeldingen/pop-ups
- OCR + Vision LLM voor interpretatie van scherminhoud
- Event hooks op applicatie-errors (bijv. browser console errors)
- Optioneel: screencast stream voor real-time observatie

**Privacy:** Alleen actief bij een actieve storingsmelding, met expliciete toestemming gebruiker.

#### B. OS Agent (Diagnose & Actie)
**Doel:** Systeemniveau diagnose en geautomatiseerde remediatie.

**Capabilities:**
- Logfile analyse (Event Viewer, syslog, applicatielogs)
- Service status checks en herstarts
- Netwerk diagnostiek (DNS, connectivity, certificaten)
- Disk/memory/CPU monitoring
- Registry/configuratie inspectie
- Geautomatiseerde fix-scripts uitvoeren

**Uitvoering:** Lightweight agent op werkstation met beperkte, gecontroleerde rechten.

#### C. Chat Widget (Interactie)
**Doel:** Communicatiekanaal tussen gebruiker en schaduwagent.

**Kenmerken:**
- Gebruiker kan in eigen woorden beschrijven wat er misgaat
- Agent communiceert in **begrijpelijke taal** (niet: "ESB storing", maar: "De koppeling tussen uw aanvraagformulier en het achterliggende systeem is tijdelijk verstoord")
- Vertaling via BlueDolphin/GGM mapping (zie BlueDolphin POC)
- Statusupdates over voortgang diagnose/oplossing

#### D. Orchestrator (LLM-kern)
**Doel:** Het brein dat alles verbindt.

**Werking:**
1. Ontvangt signalen van Screen Agent + OS Agent + Chat
2. Correleert: "Gebruiker ziet foutmelding X" + "Service Y is down" + "BlueDolphin zegt: Y is afhankelijk van Z"
3. Bepaalt diagnose met confidence score
4. Kiest actie: automatisch oplossen (hoog vertrouwen) of escaleren (laag vertrouwen)
5. Documenteert alles in TOPdesk ticket

---

## 4. Integratie met BlueDolphin & GGM

### Vertaling technisch → begrijpelijk
BlueDolphin bevat het IT-landschap: welke systemen er zijn, hoe ze samenhangen, en wat ze doen.

**Voorbeeld flow:**
```
Monitoring detecteert: "ESB-node-03 health check failed"
                              │
                              ▼
BlueDolphin lookup: ESB-node-03 → Enterprise Servicebus →
                    Koppelt: Zaaksysteem ↔ Formulierenplatform
                              │
                              ▼
GGM mapping: Zaaksysteem → "Aanvragen en meldingen"
             Formulierenplatform → "Online formulieren"
                              │
                              ▼
Gebruikersbericht: "Er is een tijdelijke storing waardoor
online formulieren voor aanvragen even niet verwerkt worden.
Uw aanvraag is bewaard en wordt automatisch verwerkt zodra
de storing is opgelost (verwacht: ~30 min)."
```

### Impact-analyse
Via BlueDolphin kan de schaduwagent automatisch bepalen:
- Welke gebruikers/afdelingen geraakt worden
- Welke processen verstoord zijn
- Wat de prioriteit moet zijn (o.b.v. werkelijke impact, niet gevoel)

---

## 5. Integratie met TOPdesk

### Slimmere ticketcreatie
De schaduwagent vervangt de slechte uitvraag door **rijke, automatische ticketregistratie:**

| Huidig (handmatig)          | Schaduwagent (automatisch)                    |
|-----------------------------|-----------------------------------------------|
| "Internet doet het niet"    | "DNS resolution faalt voor *.gemeente.nl"      |
| Categorie: "Overig"         | Categorie: "Netwerk > DNS > Resolutie"         |
| Geen bijlagen               | Screenshots + logfragmenten + systeeminfo      |
| Prioriteit: "Hoog" (gevoel) | Prioriteit: P3 (1 gebruiker, workaround beschikbaar) |
| Doorlooptijd: uren          | Doorlooptijd: minuten (auto-resolved)          |

### TOPdesk API integratie
- **Incident aanmaken** met volledige context
- **Categorisatie** op basis van werkelijke diagnose (niet gebruikersinschatting)
- **Kennisitems** automatisch aanmaken bij nieuwe oplossingen
- **Monitoring** van trends (welke storingen komen vaker voor?)

---

## 6. Scenario: Een storing van begin tot eind

```
09:01  Gebruiker opent browser, krijgt foutmelding in zaaksysteem
09:01  Screen Agent detecteert foutmelding via screenshot-analyse
09:01  OS Agent start diagnostiek: DNS ✓, Netwerk ✓, Certificaat ✓
09:02  OS Agent checkt applicatielogs: "Connection refused: esb-proxy:8443"
09:02  Orchestrator correleert met BlueDolphin: esb-proxy → ESB cluster
09:02  Orchestrator checkt monitoring API: ESB-node-03 = DOWN
09:02  Diagnose: ESB-node storing, impact op zaaksysteem
09:03  Chat Widget aan gebruiker: "We zien dat het zaaksysteem even
       niet bereikbaar is door een verstoring in een achterliggend
       systeem. Het wordt automatisch opgepakt, verwachte hersteltijd
       ~15 minuten."
09:03  TOPdesk ticket aangemaakt:
       - Categorie: Middleware > ESB > Node failure
       - Impact: Zaaksysteem, Formulierenplatform
       - CI: ESB-node-03
       - Prioriteit: P2 (meerdere processen geraakt)
       - Status: In behandeling
09:03  Actie-engine: restart ESB-node-03 service (geautomatiseerd)
09:05  OS Agent: ESB-node-03 health check = OK
09:05  Screen Agent: Zaaksysteem laadt weer correct
09:05  Chat Widget: "Het zaaksysteem werkt weer. Excuses voor het
       ongemak."
09:05  TOPdesk ticket: Status → Afgehandeld, oplossing gedocumenteerd
```

**Totale doorlooptijd: 4 minuten, zonder menselijke tussenkomst.**

---

## 7. Open Source Landschap — Wat kunnen we hergebruiken?

Uit onderzoek blijken er diverse open source projecten te zijn die als bouwstenen kunnen dienen:

### 7.1 Screen Observatie

#### ScreenPipe (mediar-ai/screenpipe)
- **GitHub:** https://github.com/mediar-ai/screenpipe
- **Wat:** Open source "Rewind.ai alternatief" — neemt continu scherm en audio op, maakt het doorzoekbaar met AI
- **Relevantie:** Kan dienen als screen capture engine. Detecteert events (app switches, clicks, foutmeldingen) en maakt screenshots alleen bij veranderingen. Heeft ingebouwde OCR en draait als MCP-server zodat Claude er direct mee kan praten
- **Licentie:** MIT
- **Status:** Actief, trending op GitHub, gebackt door Founders Inc.
- **Hergebruik:** Screen Agent component — event-driven screenshots + OCR + AI-doorzoekbaar

### 7.2 OS Agent / Systeemcontrole

#### Open Interpreter (openinterpreter/open-interpreter)
- **GitHub:** https://github.com/openinterpreter/open-interpreter
- **Wat:** Natural language interface voor computers. LLM voert code uit op je lokale machine
- **Relevantie:** Kan dienen als OS Agent — voert diagnostiek uit, leest logs, herstart services, alles via natural language instructies aan een LLM
- **Licentie:** AGPL-3.0
- **Status:** 50K+ stars, 100+ contributors
- **Hergebruik:** OS diagnose & remediatie — "check waarom service X niet draait en herstart hem"

#### Goose (block/goose)
- **GitHub:** https://github.com/block/goose
- **Wat:** On-machine AI agent van Block (Jack Dorsey). Kan complete projecten bouwen, code uitvoeren, debuggen, en interacteren met externe API's
- **Relevantie:** Gebouwd op MCP (Model Context Protocol), werkt met elke LLM, kan desktop automatisering doen. Block gebruikt "Headless Goose" in CI voor automatische vulnerability fixes
- **Licentie:** Apache 2.0
- **Status:** Actief ontwikkeld door Block
- **Hergebruik:** Agent-framework met MCP-integratie voor systeemtaken

### 7.3 TOPdesk Integratie

#### topdesk (PyPI package)
- **PyPI:** https://pypi.org/project/topdesk/
- **Wat:** Python API client voor TOPdesk REST API
- **Relevantie:** Directe integratie voor ticket aanmaken, categoriseren, bijwerken
- **Status:** v0.0.17, actief onderhouden
- **Hergebruik:** TOPdesk ticket-integratie out-of-the-box

#### TOPdeskPy (TwinkelToe/TOPdeskPy)
- **GitHub:** https://github.com/TwinkelToe/TOPdeskPy
- **Wat:** Alternatieve Python wrapper voor TOPdesk API

#### TOPdesk Developer Portal
- **URL:** https://developers.topdesk.com/
- **Wat:** Officiële REST API documentatie + tutorials. Gratis te gebruiken

### 7.4 BlueDolphin / Enterprise Architectuur

#### BlueDolphin API (ValueBlue)
- **URL:** https://www.valueblue.com/bluedolphin
- **Wat:** Enterprise architectuur tool met volledige ArchiMate support
- **API:** Public API beschikbaar voor custom integraties. Webhook service in ontwikkeling voor bidirectionele flows
- **ArchiMate:** Alle objecten en relaties zijn ArchiMate-gebaseerd, waardoor IT-landschap mapping direct bruikbaar is
- **Hergebruik:** Kennislaag voor impact-analyse en vertaling technisch → begrijpelijk

### 7.5 AIOps & Autonome Remediatie

#### Grafana SRE Agent
- **Wat:** AI assistant die meerdere databronnen (Prometheus, Loki, Tempo) bevraagt, incidenten correleert, en remediatie-stappen voorstelt
- **Relevantie:** Vendor-neutrale AIOps capabilities, kan monitoring-data leveren aan de schaduwagent
- **Hergebruik:** Monitoring-integratie laag

#### OpenTelemetry
- **URL:** https://opentelemetry.io/
- **Wat:** Gestandaardiseerde instrumentatie voor logs, metrics en traces
- **Relevantie:** Universele telemetry standaard, maakt de schaduwagent vendor-onafhankelijk
- **Hergebruik:** Telemetry-verzameling voor OS Agent

### 7.6 Agent Orchestratie Frameworks

| Framework   | Geschiktheid | Waarom                                              |
|-------------|-------------|------------------------------------------------------|
| LangGraph   | Hoog        | Stateful, multi-agent workflows met cyclische logica |
| CrewAI      | Hoog        | Role-based agents, goed voor team-achtige samenwerking |
| AutoGen     | Medium      | Microsoft's multi-agent framework, meer research-gericht |
| Claude Agent SDK | Hoog  | Native Anthropic SDK voor agent-bouw met Claude      |

---

## 8. Technische bouwstenen

### Wat te bouwen vs. hergebruiken (bijgewerkt)

| Component             | Bouwen / Hergebruiken              | Open Source Project            |
|-----------------------|------------------------------------|--------------------------------|
| Screen observatie     | **Hergebruiken**                   | ScreenPipe                     |
| OCR / Vision          | **Hergebruiken**                   | ScreenPipe OCR + Claude Vision |
| OS diagnostiek        | **Hergebruiken + aanpassen**       | Open Interpreter / Goose       |
| LLM Orchestrator      | **Bouwen** (kern-IP)              | LangGraph + Claude API         |
| TOPdesk integratie    | **Hergebruiken + uitbreiden**      | topdesk PyPI package           |
| BlueDolphin integratie| **Bouwen**                         | BlueDolphin Public API         |
| Chat widget           | **Hergebruiken**                   | Open-source chat UI            |
| Actie-engine          | **Bouwen op basis van**            | Goose / Open Interpreter       |
| Monitoring            | **Hergebruiken**                   | Grafana + OpenTelemetry        |

### Technologiestack (voorstel)
- **Backend:** Python 3.12+
- **LLM:** Claude API (Opus/Sonnet) voor redeneren, Haiku voor snelle classificatie
- **Orchestratie:** LangGraph of CrewAI voor agent-workflow
- **OS Agent:** Open Interpreter of Goose (MCP-based)
- **Screen capture:** ScreenPipe (Rust, draait als MCP-server)
- **TOPdesk:** topdesk PyPI package + custom extensies
- **BlueDolphin:** Custom client op BlueDolphin Public API
- **Monitoring:** Grafana + OpenTelemetry
- **Message queue:** Redis of NATS voor agent-communicatie
- **Database:** PostgreSQL voor kennisbank en logging

---

## 8. Toetsing: Security, WCAG & Common Ground — Comply or Explain

### 8.1 Security — BIO2 / NIS2 / EU AI-verordening

De BIO2 (vastgesteld sept 2025, v1.3 gepubliceerd maart 2026) is het verplichte normenkader voor informatiebeveiliging bij de overheid. Daarnaast geldt de EU AI-verordening (in werking sinds aug 2024) voor AI-systemen.

| Eis / Principe | Status | Toelichting |
|----------------|--------|-------------|
| **ISMS (ISO 27001)** | COMPLY | Schaduwagent wordt opgenomen in het ISMS van de organisatie. Risicoanalyse per component |
| **Risicogestuurde benadering (BIO2)** | COMPLY | Geen vaste BBN-niveaus meer; per component risicobeoordeling uitvoeren (screen agent = hoger risico dan chat widget) |
| **Least privilege** | COMPLY | OS Agent krijgt minimale rechten via service account. Alleen goedgekeurde acties in whitelist |
| **Logging & audit trail** | COMPLY | Alle agent-acties worden gelogd (wie, wat, wanneer, waarom). Conform NEN 2082 |
| **Dataminimalisatie (AVG)** | COMPLY | Screenshots alleen bij actief incident met expliciete opt-in. Automatische verwijdering na afhandeling |
| **Encryptie in transit & at rest** | COMPLY | TLS 1.3 voor alle API-communicatie. Versleutelde opslag van screenshots en logs |
| **Toegangsbeheer** | COMPLY | RBAC voor beheerders. MFA voor toegang tot orchestrator en actie-engine |
| **NIS2 / Cyberbeveiligingswet** | COMPLY | Supply chain security: open source dependencies scannen (SCA). Incidentmelding <24u bij NCSC |
| **EU AI-verordening — risicoclassificatie** | EXPLAIN | Schaduwagent is waarschijnlijk **hoog-risico** (overheids-AI die autonome besluiten neemt). Vereist: grondrechteneffectbeoordeling, registratie in EU AI-database (per aug 2026), menselijk toezicht, transparantie |
| **EU AI-verordening — transparantie** | COMPLY | Gebruiker weet dat AI meedraait. Elke actie wordt uitgelegd. Geen "black box" beslissingen |
| **EU AI-verordening — menselijk toezicht** | COMPLY | Risicovolle acties vereisen menselijke goedkeuring (approval workflow). Alleen low-risk acties zijn volledig autonoom |
| **AI-geletterdheid medewerkers** | COMPLY | Training voor beheerders en gebruikers over werking schaduwagent (eis vanuit AI-verordening) |
| **DPIA (Data Protection Impact Assessment)** | COMPLY | Verplicht vanwege schermobservatie. Uitvoeren vóór POC-start |
| **Lokale verwerking** | COMPLY | Screen analyse op werkstation waar mogelijk. LLM-calls naar API bevatten geanonimiseerde/geminimaliseerde data |

**Belangrijkste aandachtspunt:** De schaduwagent valt vrijwel zeker onder **hoog-risico AI** vanwege overheidsinzet met autonome acties. Dit betekent:
- Grondrechteneffectbeoordeling vóór ingebruikname
- Registratie in EU AI-database vóór augustus 2026
- Conformiteitsbeoordeling
- Continue monitoring en logging van AI-beslissingen

---

### 8.2 WCAG — Digitale Toegankelijkheid

Wettelijk verplicht: **WCAG 2.1 niveau A en AA** (via EN 301 549 / Wet digitale overheid). WCAG 2.2 is aanbevolen maar nog niet verplicht.

| WCAG Eis | Component | Status | Toelichting |
|----------|-----------|--------|-------------|
| **Perceivable (waarneembaar)** | Chat Widget | COMPLY | Tekstalternatieven voor niet-tekst content, voldoende contrast, aanpasbare tekst |
| **Operable (bedienbaar)** | Chat Widget | COMPLY | Volledig bedienbaar met toetsenbord. Geen tijdslimieten op gebruikersinteractie |
| **Understandable (begrijpelijk)** | Chat Widget | COMPLY | Taal is begrijpelijk (kernfunctie!). Voorspelbaar gedrag. Foutherstel |
| **Robust** | Chat Widget | COMPLY | Compatibel met hulptechnologieën (screenreaders). Semantische HTML |
| **WCAG 2.2 — Focus appearance** | Chat Widget | COMPLY | Nieuwe eis in 2.2: duidelijke focusindicator. Nemen we mee |
| **WCAG 2.2 — Dragging movements** | Chat Widget | COMPLY | Alternatieven voor drag-acties |
| **Screen Agent output** | Statusberichten | COMPLY | Statusupdates via ARIA live regions, ook bruikbaar voor screenreaders |
| **Meertaligheid** | Chat Widget | EXPLAIN | Initieel alleen Nederlands. Uitbreiding naar andere talen in latere fase. Geen barrière voor gebruik maar beperkt bereik |
| **Cognitieve toegankelijkheid** | Alle UI | COMPLY | Eenvoudige taal, duidelijke stappen, geen jargon — dit is juist de kernwaarde van de schaduwagent |

**Scope:** WCAG is van toepassing op de **Chat Widget** (het gebruikersinterface-deel). De Screen Agent en OS Agent zijn backend-componenten zonder directe gebruikersinteractie en vallen niet onder WCAG. Het **beheerdersinterface** (dashboard, configuratie) valt wél onder WCAG.

---

### 8.3 Common Ground — VNG Architectuurprincipes

Common Ground is de VNG-architectuurvisie voor gemeentelijke IT. Principes getoetst:

| Common Ground Principe | Status | Toelichting |
|------------------------|--------|-------------|
| **Componentgebaseerd** | COMPLY | Schaduwagent is opgebouwd uit losse componenten (Screen Agent, OS Agent, Orchestrator, Chat Widget). Elk component is zelfstandig vervangbaar |
| **Gegevens bij de bron** | COMPLY | Geen kopieën van data. BlueDolphin wordt bevraagd bij de bron. TOPdesk is de bron voor tickets. OS-data wordt realtime gelezen, niet gekopieerd |
| **Open standaarden** | COMPLY | OpenAPI specificaties voor alle API's. ArchiMate voor architectuurmodellen. OpenTelemetry voor monitoring |
| **Open source** | COMPLY | Kern-componenten worden open source ontwikkeld (Apache 2.0, conform LICENSE in deze repo). Hergebruik van bestaande open source projecten |
| **5-lagenmodel** | COMPLY | Schaduwagent past in het 5-lagenmodel: interactielaag (chat widget), proceslaag (orchestrator), integratielaag (API's), servicelaag (agents), datalaag (kennisbank) |
| **API-first** | COMPLY | Alle communicatie tussen componenten via REST API's met OpenAPI specs. TOPdesk en BlueDolphin via hun publieke API's |
| **FSC (Federatieve Service Connectiviteit)** | EXPLAIN | FSC vervangt NLX sinds 2025 als standaard in de integratielaag. Voor de POC gebruiken we directe API-calls. FSC-compliance wordt meegenomen in Fase 3 (BlueDolphin/GGM integratie) wanneer we het gemeentelijke datalandschap aansluiten |
| **GEMMA Gegevenslandschap** | COMPLY | GGM (Gemeentelijk Gegevensmodel) wordt gebruikt voor vertaling technisch → begrijpelijk. BlueDolphin ondersteunt ArchiMate wat aansluit op GEMMA |
| **ZGW API's (Zaakgericht Werken)** | EXPLAIN | Schaduwagent maakt incidenttickets aan in TOPdesk, niet in een zaaksysteem. Als de gemeente incidenten als zaken wil registreren, kan ZGW API-integratie in een latere fase worden toegevoegd |
| **Community-gedreven ontwikkeling** | COMPLY | Open source repo, samenwerking met andere gemeenten mogelijk. Referentie-implementatie beschikbaar stellen |
| **Privacy by design** | COMPLY | DPIA vooraf, dataminimalisatie, opt-in schermobservatie, automatische opschoning |
| **NLDesign System** | EXPLAIN | Voor de Chat Widget is het wenselijk om NL Design System componenten te gebruiken voor een herkenbare overheidslook-and-feel. Dit wordt meegenomen in Fase 2 bij de chat widget-ontwikkeling |

---

### 8.4 Samenvatting: Comply or Explain

```
COMPLY:  25 van 30 eisen ✓
EXPLAIN:  5 van 30 eisen (met mitigatieplan)

EXPLAIN items en planning:
1. EU AI-verordening hoog-risico    → Grondrechteneffectbeoordeling in Fase 1
2. Meertaligheid (WCAG)             → Nederlands eerst, uitbreiden in Fase 5
3. FSC (Common Ground)              → Directe API's in POC, FSC in Fase 3
4. ZGW API's (Common Ground)        → TOPdesk-first, ZGW optioneel in Fase 5
5. NL Design System (Common Ground) → Meenemen in Fase 2 (Chat Widget)
```

---

### 8.5 Security-specifieke maatregelen

#### Architectuur security
- **Zero Trust model** — geen component vertrouwt een ander component impliciet
- **API Gateway** — alle externe API-calls via gateway met rate limiting, auth en logging
- **Secrets management** — API keys en credentials in vault (HashiCorp Vault of Azure Key Vault)
- **Network segmentation** — OS Agent communiceert via dedicated, versleuteld kanaal met backend

#### OS Agent security (kritisch component)
- **Whitelist-only acties** — OS Agent kan alleen vooraf goedgekeurde commando's uitvoeren
- **Sandboxing** — agent draait in geïsoleerde context (container of restricted shell)
- **Geen persistentie** — agent bewaart geen credentials of gevoelige data lokaal
- **Code signing** — alle fix-scripts zijn getekend en geverifieerd voor uitvoering
- **Kill switch** — beheerder kan agent per direct uitschakelen via beheerinterface

#### Screen Agent security
- **Opt-in per sessie** — gebruiker moet per incident toestemmen
- **PII-detectie** — automatische detectie en blurring van BSN, wachtwoorden, financiële data
- **Tijdsgebonden** — screenshots worden na ticketafhandeling automatisch verwijderd
- **Geen opslag van volledige schermvideo** — alleen event-driven snapshots

#### Supply chain security
- **SBOM (Software Bill of Materials)** — voor alle dependencies
- **Dependency scanning** — automatische CVE-checks (Dependabot/Renovate)
- **Container image scanning** — bij gebruik van containers (Trivy/Grype)

---

## 9. Fasering

### Fase 1: POC (4-6 weken)
- Eenvoudige OS Agent: logfile analyse + service checks
- Basis LLM orchestrator met Claude API
- TOPdesk ticket aanmaken via API met rijke context
- Scope: 1 specifieke storing-type (bijv. "applicatie niet bereikbaar")

### Fase 2: Screen Observatie (4-6 weken)
- Screen Agent integratie
- Vision-model voor schermanalyse
- Correlatie scherm ↔ systeemdata
- Chat widget voor gebruikersinteractie

### Fase 3: BlueDolphin & GGM (3-4 weken)
- BlueDolphin API koppeling
- IT-landschap mapping voor impact-analyse
- Vertaling technisch → begrijpelijk via GGM
- Uitbreiding naar meerdere storingstypen

### Fase 4: Geautomatiseerde Remediatie (4-6 weken)
- Actie-engine met goedgekeurde fix-scripts
- Approval workflow voor risicovolle acties
- Kennisbank opbouw (elke oplossing = nieuw kennisitem)
- Monitoring-integratie (Zabbix/PRTG)

### Fase 5: Productie & Schaal (doorlopend)
- Uitrol naar alle werkplekken
- Continue verbetering op basis van feedback
- Uitbreiding storingstypen en remediatie-scripts
- Rapportage en dashboards voor beheersorganisatie

---

## 10. Waarom dit werkt voor de beheersorganisatie

1. **Lagere MTTR** — problemen worden in minuten opgelost, niet uren
2. **Betere data** — tickets bevatten werkelijke technische context
3. **Minder escalaties** — veelvoorkomende problemen automatisch opgelost
4. **Inzicht in patronen** — welke storingen komen vaker voor, waar ligt de oorzaak?
5. **Gebruikerstevredenheid** — geen frustrerende uitvraag, snelle oplossing
6. **Kennisbehoud** — oplossingen worden vastgelegd, niet verloren in hoofden van specialisten
7. **Schaalbaarheid** — de agent kan oneindig veel gebruikers tegelijk helpen

---

## 11. Relatie met de andere initiatieven

| Initiatief                        | Relatie met Schaduwagent                                      |
|-----------------------------------|---------------------------------------------------------------|
| BlueDolphin POC (vertaling → GGM) | Levert de vertaallaag: technisch → begrijpelijk               |
| TOPdesk categorisering            | Schaduwagent levert de data voor betere categorisering        |
| Enthousiasme beheersorganisatie   | Schaduwagent is het meest zichtbare, tastbare resultaat       |

De vier ideeën vormen samen één geheel: de schaduwagent is het **platform**, BlueDolphin/GGM is de **kennislaag**, en betere TOPdesk-categorisering is het **resultaat**.
