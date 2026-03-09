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

## 8. Privacy & Security

### Principes
1. **Minimale dataverzameling** — screenshots alleen bij actief incident
2. **Toestemming gebruiker** — expliciete opt-in voor schermobservatie
3. **Lokale verwerking waar mogelijk** — screen analyse op werkstation
4. **Audit trail** — alle acties gelogd en traceerbaar
5. **Least privilege** — OS Agent heeft alleen rechten die nodig zijn
6. **Data classificatie** — gevoelige informatie op scherm wordt geblurd/gefilterd

### BIO/NEN compliance
- Verwerking conform AVG/GDPR
- Logging conform NEN 2082 (archiveringsstandaard)
- Toegangsbeheer conform BIO (Baseline Informatiebeveiliging Overheid)

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
