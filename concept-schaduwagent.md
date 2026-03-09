# Concept: De Schaduwagent — AI-gestuurd Incidentbeheer

> **Uitgangspunten:** 100% open source | Minimale US footprint | EU-soevereiniteit waar mogelijk | Claude als analyse-agent via EU-regio

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
│  │  │ CMDB          │  │  │  - Config aanpassing        │      │
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
│  │   Integraties (alle open source)                         │   │
│  │  ┌──────────┐ ┌──────────────┐ ┌───────────────────┐    │   │
│  │  │ TOPdesk  │ │ CMDBuild     │ │ Monitoring        │    │   │
│  │  │ API      │ │ (of BlueDolp)│ │ (Zabbix/PRTG/etc) │    │   │
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
- Vertaling via CMDB/GGM mapping (CMDBuild of optioneel BlueDolphin)
- Statusupdates over voortgang diagnose/oplossing

#### D. Orchestrator (LLM-kern)
**Doel:** Het brein dat alles verbindt.

**Werking:**
1. Ontvangt signalen van Screen Agent + OS Agent + Chat
2. Correleert: "Gebruiker ziet foutmelding X" + "Service Y is down" + "CMDB zegt: Y is afhankelijk van Z"
3. Bepaalt diagnose met confidence score
4. Kiest actie: automatisch oplossen (hoog vertrouwen) of escaleren (laag vertrouwen)
5. Documenteert alles in TOPdesk ticket

---

## 4. Integratie met CMDB & GGM

### Vertaling technisch → begrijpelijk
De CMDB (CMDBuild, open source — of optioneel BlueDolphin) bevat het IT-landschap: welke systemen er zijn, hoe ze samenhangen, en wat ze doen.

**Voorbeeld flow:**
```
Monitoring detecteert: "ESB-node-03 health check failed"
                              │
                              ▼
CMDB lookup: ESB-node-03 → Enterprise Servicebus →
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
Via de CMDB kan de schaduwagent automatisch bepalen:
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
09:02  Orchestrator correleert met CMDB: esb-proxy → ESB cluster
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

### 7.1 Screen Observatie & Computer Use

#### ScreenPipe (screenpipe/screenpipe) — AANBEVOLEN
- **GitHub:** https://github.com/mediar-ai/screenpipe
- **Wat:** Open source "Rewind.ai alternatief" — neemt continu scherm en audio op, maakt het doorzoekbaar met AI. 12.600+ stars, $2.8M funding
- **Relevantie:** Detecteert events (app switches, clicks, foutmeldingen) en maakt screenshots alleen bij veranderingen. Heeft ingebouwde OCR en draait als **MCP-server** zodat Claude er direct mee kan praten. Bevat ook "screenpipe terminator" (Playwright-achtige desktop automatisering)
- **Licentie:** MIT
- **Hergebruik:** Screen Agent component — event-driven screenshots + OCR + AI-doorzoekbaar + MCP

#### Agent S (simular-ai/Agent-S)
- **GitHub:** https://github.com/simular-ai/Agent-S
- **Wat:** Open-source framework voor autonome GUI-interactie. Agent S3 overtreft menselijke prestaties op OSWorld benchmark (72.6%)
- **Relevantie:** Kan als "handen" dienen voor de screen observatie-laag — begrijpt en interacteert met GUIs, navigeert foutdialogen, leest applicatiestatus
- **Licentie:** Apache 2.0

#### UI-TARS Desktop (ByteDance)
- **GitHub:** https://github.com/bytedance/UI-TARS-desktop
- **Wat:** Multimodale AI agent-stack die vision-modellen verbindt met terminal, computer, browser. Bevat Remote Computer Operator en Remote Browser Operator
- **Licentie:** Apache 2.0

### 7.2 OS Agent / Systeemcontrole

#### Open Interpreter (openinterpreter/open-interpreter)
- **GitHub:** https://github.com/openinterpreter/open-interpreter
- **Wat:** Natural language interface voor computers. LLM voert code uit op je lokale machine — shell, Python, JavaScript. Volledige toegang tot filesystem en netwerk
- **Relevantie:** OS Agent — voert diagnostiek uit, leest logs, herstart services via natural language
- **Licentie:** AGPL-3.0
- **Status:** 50K+ stars, 100+ contributors

#### Goose (block/goose) — AANBEVOLEN
- **GitHub:** https://github.com/block/goose
- **Wat:** On-machine AI agent van Block. Gebouwd op **MCP**, werkt met elke LLM. Block gebruikt "Headless Goose" in CI voor automatische vulnerability fixes. Lid van Linux Foundation's Agentic AI Foundation
- **Licentie:** Apache 2.0
- **Hergebruik:** MCP-native agent-framework. TOPdesk en BlueDolphin als MCP-servers = direct toegankelijk

### 7.3 Actie-engine / Geautomatiseerde Remediatie

#### Ansible AWX — AANBEVOLEN
- **GitHub:** https://github.com/ansible/awx
- **Wat:** Open-source web UI, REST API en task engine voor Ansible. Job scheduling, RBAC, credential management, workflow orchestratie met approval steps
- **Relevantie:** Perfecte actie-engine. Pre-approved Ansible playbooks voor service herstarts, config fixes, netwerk resets. AWX workflows bevatten approval gates voor risicovolle acties. Event-Driven Ansible kan playbooks automatisch triggeren
- **Licentie:** Apache 2.0
- **Status:** Mature project, upstream van Red Hat Ansible Automation Platform

#### StackStorm (ST2)
- **GitHub:** https://github.com/StackStorm/st2
- **Wat:** Event-driven automatiseringsplatform ("IFTTT for Ops") voor auto-remediatie. Rules engine, workflow engine, 160 integratiepacks met 6.000+ acties, ChatOps
- **Relevantie:** Bewezen event-driven remediatie. Sensors detecteren events → rules triggeren acties. Gebruikt door Netflix, Target, CERN
- **Licentie:** Apache 2.0
- **Status:** 6.400+ stars, Linux Foundation

### 7.4 TOPdesk Integratie

#### topdesk (PyPI package)
- **PyPI:** https://pypi.org/project/topdesk/
- **Wat:** Python API client voor TOPdesk REST API
- **Relevantie:** Directe integratie voor ticket aanmaken, categoriseren, bijwerken
- **Licentie:** GPL-3.0
- **Status:** v0.0.17

#### TOPdeskPy & topdesk-api-python
- https://github.com/TwinkelToe/TOPdeskPy
- https://github.com/DigizoneICT/topdesk-api-python
- Alternatieve Python wrappers

#### TOPdesk Developer Portal
- **URL:** https://developers.topdesk.com/
- Officiële REST API documentatie + tutorials. Gratis te gebruiken

### 7.5 CMDB / Enterprise Architectuur

#### CMDBuild — AANBEVOLEN (open source)
- **URL:** https://www.cmdbuild.org/
- **Wat:** Open-source CMDB voor asset management. Configureerbare workflows, rapporten, webservices, REST API. Java/PostgreSQL
- **Relevantie:** Vervangt BlueDolphin als open-source CMDB voor IT-landschap mapping, impact-analyse, en CI-relaties. Volledig self-hosted, EU-soeverein
- **Licentie:** AGPL
- **Hergebruik:** Kennislaag voor impact-analyse en vertaling technisch → begrijpelijk via GGM-mapping

#### BlueDolphin API (ValueBlue) — OPTIONEEL
- **URL:** https://www.valueblue.com/bluedolphin
- **Wat:** Commercieel enterprise architectuur tool met ArchiMate/BPMN support
- **Let op:** **Niet open-source.** Alleen als koppeling als de organisatie BlueDolphin al gebruikt. Integratie via Public API

### 7.6 AIOps & Monitoring

#### Keep (keephq/keep) — AANBEVOLEN
- **GitHub:** https://github.com/keephq/keep
- **Wat:** Open-source AIOps en alert management platform. Single pane of glass voor alerts van elke monitoring tool. Alert deduplicatie, verrijking, correlatie, workflow automatisering
- **Relevantie:** Centrale alert-aggregatie. Correleert alerts van Zabbix/PRTG/Grafana tot betekenisvolle incidenten. YAML-based workflow automation kan de schaduwagent triggeren
- **Licentie:** MIT
- **Status:** 11.500+ stars, Y Combinator backed

#### Grafana SRE Agent
- **Wat:** AI assistant die Prometheus, Loki, Tempo bevraagt, incidenten correleert, remediatie voorstelt
- **Hergebruik:** Monitoring-integratie laag

#### OpenTelemetry
- **URL:** https://opentelemetry.io/
- **Wat:** Universele telemetry standaard voor logs, metrics en traces
- **Hergebruik:** Vendor-onafhankelijke telemetry-verzameling

#### LogAI (Salesforce)
- **GitHub:** https://github.com/salesforce/logai
- **Wat:** One-stop library voor log analytics en intelligence. Log summarization, clustering, anomaly detection
- **Licentie:** BSD 3-Clause
- **Hergebruik:** OS Agent's log-analyse backend

### 7.7 Agent Orchestratie Frameworks

| Framework   | Geschiktheid | Waarom                                              |
|-------------|-------------|------------------------------------------------------|
| **LangGraph** | **Hoog** | Stateful, multi-agent workflows met cyclische logica. Referentie-implementatie bestaat: "Autonomous AI Sysadmin" met LangGraph + Ansible |
| **CrewAI** | **Hoog** | Role-based agents met geheugen. Natuurlijke mapping: Screen Observer, System Diagnostician, Ticket Creator, Remediator als crew |
| AutoGen | Medium | Microsoft's multi-agent framework, 40K+ stars. Docker-based code execution voor veilige remediatie |
| Claude Agent SDK | Hoog | Native Anthropic SDK voor agent-bouw met Claude |

#### Referentie-architectuur
Er bestaat een direct toepasbare referentie-implementatie: **"Autonomous AI Sysadmin with LangGraph + Ansible + RHEL 9"** die exact het OS Agent + Orchestrator patroon implementeert:
- Ansible verzamelt telemetry en voert remediatie-playbooks uit
- Python + SQLite berekent baselines en detecteert anomalieën
- LangGraph beheert de stateful workflow — beslist: auto-heal of escaleren
- Gemini (vervangbaar door Claude) doet root cause analysis

### 7.8 Chat Widget & Ticket AI

#### Chatwoot — AANBEVOLEN
- **GitHub:** https://github.com/chatwoot/chatwoot
- **Wat:** AI-powered, open-source customer support platform. Self-host of cloud. Alternatief voor Intercom/Zendesk
- **Relevantie:** Chat Widget component met ingebouwde AI, multi-channel support, agent dashboard
- **Licentie:** MIT
- **Status:** 20.000+ stars

#### Open Ticket AI
- **GitHub:** https://github.com/Softoft-Orga/open-ticket-ai
- **Wat:** Open-source, on-premise AI engine voor ticket classificatie, routing en verwerking. Draait in Docker, ondersteunt lokale LLMs via Ollama
- **Relevantie:** Geautomatiseerde ticket-classificatie, prioriteitsbepaling, taal/sentiment-analyse. GDPR-compliant met lokale LLM optie

### 7.9 Integratie & Connectiviteit

#### MCP (Model Context Protocol) — KERNSTANDAARD
- **URL:** https://modelcontextprotocol.io/
- **Wat:** Open standaard van Anthropic (nu onder Linux Foundation) voor het verbinden van LLMs met externe tools/data. JSON-RPC 2.0 gebaseerd. 16.000+ MCP servers beschikbaar
- **Relevantie:** De "universele adapter" voor de schaduwagent. ScreenPipe heeft al een MCP server. Goose is gebouwd op MCP. TOPdesk en BlueDolphin als MCP servers bouwen maakt ze direct toegankelijk voor elke MCP-compatible agent
- **Licentie:** Apache 2.0

#### Apache Airflow — AANBEVOLEN
- **GitHub:** https://github.com/apache/airflow
- **Wat:** Workflow orchestratie platform. DAG-based, uitbreidbaar met operators, 60.000+ stars. Apache Foundation project
- **Relevantie:** Integratielaag: monitoring alert → log extractie → LLM voor RCA → TOPdesk ticket. Scheduling, retry-logica, monitoring dashboard
- **Licentie:** Apache 2.0 (volledig open source)

#### n8n (alternatief, let op licentie)
- **GitHub:** https://github.com/n8n-io/n8n
- **Wat:** Workflow automatisering met 400+ integraties en native AI nodes. Self-hostable. 60.000+ stars
- **Let op:** **Fair-code licentie (Sustainable Use License) — geen OSI-goedgekeurde open source.** Bruikbaar voor evaluatie, maar commercieel gebruik vereist licentie

---

## 8. Technische bouwstenen

### Wat te bouwen vs. hergebruiken — 100% open source

| Component             | Bouwen / Hergebruiken              | Aanbevolen Open Source           | Licentie     | EU-hosted? |
|-----------------------|------------------------------------|----------------------------------|--------------|------------|
| Screen observatie     | **Hergebruiken**                   | ScreenPipe + Agent S             | MIT / Apache 2.0 | Ja (lokaal) |
| OCR / Vision          | **Hergebruiken**                   | ScreenPipe OCR + Claude Vision   | MIT          | Ja (lokaal) |
| OS diagnostiek        | **Hergebruiken + aanpassen**       | Goose (MCP-based)                | Apache 2.0   | Ja (lokaal) |
| LLM Analyse-agent     | **Claude** via EU-regio            | Claude API (Bedrock EU)          | Commercieel  | Ja (EU-regio) |
| LLM Fallback          | **Hergebruiken**                   | Mistral (self-hosted)            | Apache 2.0   | Ja (lokaal) |
| LLM Orchestrator      | **Bouwen** (kern-IP)              | LangGraph                        | MIT          | Ja (lokaal) |
| Actie-engine          | **Hergebruiken + configureren**    | Ansible AWX of StackStorm        | Apache 2.0   | Ja (lokaal) |
| TOPdesk integratie    | **Hergebruiken + MCP server**      | topdesk PyPI + custom MCP        | GPL-3.0      | Ja         |
| CMDB                  | **Hergebruiken**                   | CMDBuild                         | AGPL         | Ja (lokaal) |
| Chat widget           | **Hergebruiken**                   | Chatwoot                         | MIT          | Ja (lokaal) |
| Alert aggregatie      | **Hergebruiken**                   | Keep                             | MIT          | Ja (lokaal) |
| Log analyse           | **Hergebruiken**                   | LogAI (Salesforce)               | BSD 3-Clause | Ja (lokaal) |
| Ticket classificatie  | **Hergebruiken**                   | Open Ticket AI + Ollama          | Open Source  | Ja (lokaal) |
| Monitoring            | **Hergebruiken**                   | Grafana + OpenTelemetry          | AGPLv3/Apache| Ja (lokaal) |
| Workflow integratie   | **Hergebruiken**                   | Apache Airflow                   | Apache 2.0   | Ja (lokaal) |
| Tool connectiviteit   | **Standaard**                      | MCP (Model Context Protocol)     | Apache 2.0   | Ja (lokaal) |

### Technologiestack (voorstel)
- **Backend:** Python 3.12+
- **Analyse-agent (LLM):** Claude API via AWS Bedrock EU-regio (Frankfurt/Ierland) — data blijft in EU
- **LLM fallback/lokaal:** Mistral Large (Apache 2.0, Frans/EU, self-hosted via Ollama/vLLM)
- **Snelle classificatie:** Mistral Small via Ollama (volledig lokaal, geen data naar buiten)
- **Orchestratie:** LangGraph voor stateful agent-workflows
- **OS Agent:** Goose (MCP-native, Apache 2.0)
- **Actie-engine:** Ansible AWX met approval workflows
- **Screen capture:** ScreenPipe (Rust, MCP-server)
- **Chat widget:** Chatwoot (MIT, self-hosted)
- **CMDB:** CMDBuild (AGPL, self-hosted, Java/PostgreSQL)
- **Alert aggregatie:** Keep (AIOps platform)
- **TOPdesk:** topdesk PyPI package + custom MCP server
- **Log analyse:** LogAI voor anomaly detection
- **Monitoring:** Grafana + OpenTelemetry
- **Workflow:** Apache Airflow (Apache 2.0)
- **Tool connectivity:** MCP als universele adapter
- **Database:** PostgreSQL voor kennisbank en logging
- **Hosting:** Volledig on-premise of EU-cloud (geen US-datacenters)

---

## 8a. EU-soevereiniteit & Open Source Strategie

### Uitgangspunt
Alle componenten zijn open source (OSI-goedgekeurd). De enige uitzondering is de Claude API als analyse-agent, die via EU-regio's wordt aangeroepen zodat data in de EU blijft.

### LLM-strategie: gelaagd model

```
┌─────────────────────────────────────────────────────────────┐
│                    LLM GELAAGD MODEL                         │
│                                                             │
│  Laag 1: LOKAAL (geen data naar buiten)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Mistral Small / Mistral NeMo via Ollama                │ │
│  │ → Snelle classificatie, triage, eenvoudige diagnose    │ │
│  │ → 100% on-premise, geen netwerk nodig                  │ │
│  │ → Apache 2.0, Frans/EU bedrijf                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  Laag 2: EU-REGIO (data blijft in EU)                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Claude (Opus/Sonnet) via AWS Bedrock EU-regio          │ │
│  │ → Complexe redenering, root cause analysis, correlatie │ │
│  │ → EU inference profiles: Frankfurt, Ierland, Spanje    │ │
│  │ → Data verwerking + opslag binnen EU                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  Laag 3: FALLBACK SOEVEREIN (optioneel)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Mistral Large via vLLM (self-hosted)                   │ │
│  │ → Volledige fallback als Claude niet beschikbaar       │ │
│  │ → Of voor organisaties die 0% US-verkeer willen        │ │
│  │ → Apache 2.0, volledig on-premise                      │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Waarom Claude als analyse-agent?
- **Kwaliteit:** Claude Opus/Sonnet levert de beste resultaten voor complexe redenering, correlatie van schermbeelden met systeemdata, en root cause analysis
- **MCP-native:** Claude ondersteunt MCP natively — directe integratie met ScreenPipe, Goose, en custom MCP-servers
- **EU-beschikbaar:** Via AWS Bedrock EU inference profiles (Frankfurt, Ierland, Spanje) blijft alle data binnen de EU
- **Minimale US footprint:** Alleen het model zelf is van Anthropic (US). Data verlaat de EU niet

### Waarom Mistral als lokale/fallback laag?
- **EU-soeverein:** Mistral AI is Frans, Apache 2.0 gelicenseerd, expliciet gericht op EU-soevereiniteit
- **Self-hostable:** Draait volledig on-premise via Ollama, vLLM, of llama.cpp
- **Efficiënt:** Mistral Small draait op consumer-hardware voor snelle triage
- **CLOUD Act vrij:** Geen US-bedrijf, dus geen CLOUD Act risico

### Open source audit: alle componenten

| Component | Project | Licentie | OSI-goedgekeurd? | Herkomst |
|-----------|---------|----------|-------------------|----------|
| Screen capture | ScreenPipe | MIT | Ja | VS (maar lokaal draaiend) |
| GUI interactie | Agent S | Apache 2.0 | Ja | VS (maar lokaal draaiend) |
| OS Agent | Goose | Apache 2.0 | Ja | VS (Block, maar lokaal) |
| Orchestratie | LangGraph | MIT | Ja | VS (LangChain) |
| Actie-engine | Ansible AWX | Apache 2.0 | Ja | VS (Red Hat, maar self-hosted) |
| CMDB | CMDBuild | AGPL | Ja | **Italië** (EU) |
| Chat widget | Chatwoot | MIT | Ja | **India** (self-hosted) |
| Alert platform | Keep | MIT | Ja | **Israël** (self-hosted) |
| Log analyse | LogAI | BSD 3-Clause | Ja | VS (Salesforce, maar self-hosted) |
| Ticket AI | Open Ticket AI | Open Source | Ja | **Duitsland** (EU) |
| Monitoring | Grafana | AGPL v3 | Ja | **Zweden** (EU) |
| Telemetry | OpenTelemetry | Apache 2.0 | Ja | CNCF (vendor-neutraal) |
| Workflow | Apache Airflow | Apache 2.0 | Ja | Apache Foundation |
| Connectiviteit | MCP | Apache 2.0 | Ja | Linux Foundation |
| LLM lokaal | Mistral | Apache 2.0 | Ja | **Frankrijk** (EU) |
| LLM analyse | Claude API | Commercieel | Nee* | VS (Anthropic) |
| Database | PostgreSQL | PostgreSQL | Ja | Internationaal |

*\*Claude API is de enige niet-OSI component. Mitigatie: data blijft in EU via Bedrock. Fallback naar Mistral Large (Apache 2.0) beschikbaar.*

### Dataresidentie-garanties

| Datastroom | Waar verwerkt? | Waar opgeslagen? | US-verkeer? |
|------------|----------------|------------------|-------------|
| Screenshots | Lokaal werkstation | Lokaal / EU-server | Nee |
| OS diagnostiek | Lokaal werkstation | EU-server | Nee |
| LLM triage (Mistral) | Lokaal / EU-server | Niet opgeslagen | Nee |
| LLM analyse (Claude) | AWS Bedrock EU (Frankfurt) | Niet opgeslagen* | Nee |
| TOPdesk tickets | TOPdesk cloud (EU) | TOPdesk cloud (EU) | Nee |
| CMDB data | Self-hosted EU | Self-hosted EU | Nee |
| Kennisbank | PostgreSQL EU | PostgreSQL EU | Nee |

*\*AWS Bedrock EU inference profiles: verwerking en opslag binnen EU. Geen cross-region routing.*

---

## 8b. Toetsing: Security, WCAG & Common Ground — Comply or Explain

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
| **Gegevens bij de bron** | COMPLY | Geen kopieën van data. CMDB wordt bevraagd bij de bron. TOPdesk is de bron voor tickets. OS-data wordt realtime gelezen, niet gekopieerd |
| **Open standaarden** | COMPLY | OpenAPI specificaties voor alle API's. ArchiMate voor architectuurmodellen. OpenTelemetry voor monitoring |
| **Open source** | COMPLY | **Alle** componenten zijn open source (Apache 2.0, MIT, AGPL). Enige uitzondering: Claude API via EU Bedrock, met Mistral als open source fallback |
| **5-lagenmodel** | COMPLY | Schaduwagent past in het 5-lagenmodel: interactielaag (chat widget), proceslaag (orchestrator), integratielaag (API's), servicelaag (agents), datalaag (kennisbank) |
| **API-first** | COMPLY | Alle communicatie tussen componenten via REST API's met OpenAPI specs. TOPdesk en CMDBuild via hun API's |
| **FSC (Federatieve Service Connectiviteit)** | EXPLAIN | FSC vervangt NLX sinds 2025 als standaard in de integratielaag. Voor de POC gebruiken we directe API-calls. FSC-compliance wordt meegenomen bij opschaling wanneer we het gemeentelijke datalandschap aansluiten |
| **GEMMA Gegevenslandschap** | COMPLY | GGM (Gemeentelijk Gegevensmodel) wordt gebruikt voor vertaling technisch → begrijpelijk. CMDBuild kan ArchiMate-achtige relaties vastleggen die aansluiten op GEMMA |
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

## 9. Fasering — Van stand-alone POC naar productie

### Inspiratie: NanoClaw als blauwdruk
[NanoClaw](https://github.com/qwibitai/nanoclaw) (MIT, 8.6K stars) biedt een bruikbaar patroon voor de POC:
- **~3.900 regels code** — klein genoeg om volledig te begrijpen en auditen
- **Container-isolatie** — agents draaien in Linux containers, veilig sandboxed
- **Anthropic Agent SDK** — direct gebouwd op Claude's agent-framework
- **Messaging-kanalen** — plug-in architectuur voor chat (WhatsApp, Slack, etc.)
- **Agent Swarms** — meerdere gespecialiseerde agents die samenwerken
- **SQLite geheugen** — per-sessie context en kennisopbouw

Het NanoClaw-patroon (channels → SQLite → polling loop → container agent → response) kan als startpunt dienen voor de schaduwagent. De containerisatie is direct bruikbaar voor veilige OS Agent executie.

---

### Fase 0: Stand-alone POC — "1 medewerker, 1 werkstation, 1 storing" (2-3 weken)

**Scope:** Een servicedeskmedewerker zit naast een werkstation met een storing. De schaduwagent draait op een laptop/server en helpt bij diagnose en oplossing.

**Setup:**
```
┌──────────────────┐     ┌──────────────────────────────┐
│ WERKSTATION      │     │ SCHADUWAGENT (laptop/server)  │
│ (met storing)    │     │                              │
│                  │ SSH │ ┌──────────────────────────┐ │
│                  │◄───►│ │ OS Agent (in container)  │ │
│                  │     │ │ - Leest logs             │ │
│                  │     │ │ - Checkt services        │ │
│                  │     │ │ - Doet diagnostiek       │ │
│                  │     │ └──────────┬───────────────┘ │
│                  │     │            │                  │
│                  │     │ ┌──────────▼───────────────┐ │
│                  │     │ │ Claude (analyse-agent)   │ │
│                  │     │ │ via Bedrock EU           │ │
│                  │     │ │ - Root cause analysis    │ │
│                  │     │ │ - Voorgestelde oplossing │ │
│                  │     │ └──────────┬───────────────┘ │
│                  │     │            │                  │
│                  │     │ ┌──────────▼───────────────┐ │
│                  │     │ │ Terminal UI              │ │
│                  │     │ │ (voor SD-medewerker)     │ │
│                  │     │ └──────────────────────────┘ │
└──────────────────┘     └──────────────────────────────┘
```

**Wat wordt gebouwd:**
- OS Agent gebaseerd op NanoClaw/Goose patroon: draait in container, SSH naar werkstation
- Claude via Bedrock EU als analyse-agent: ontvangt systeemdata, doet diagnose
- Eenvoudige terminal/CLI interface voor de servicedeskmedewerker
- Geen fancy UI, geen integraties — puur: "kijk mee en help oplossen"

**Wat de SD-medewerker ervaart:**
```
$ schaduwagent connect 192.168.1.42

[Schaduwagent] Verbonden met werkstation. Bezig met analyse...
[Schaduwagent] Systeeminfo: Windows 11 Pro, 16GB RAM, domein: gemeente.local
[Schaduwagent] Checking services...
[Schaduwagent] ⚠ Service 'esb-proxy' status: STOPPED (crash 5 min geleden)
[Schaduwagent] Loganalyse: OutOfMemoryException in esb-proxy.log
[Schaduwagent]
[Schaduwagent] DIAGNOSE: ESB proxy service is gecrasht door geheugenprobleem.
[Schaduwagent] Dit verklaart waarom het zaaksysteem niet bereikbaar is.
[Schaduwagent]
[Schaduwagent] VOORGESTELDE ACTIE:
[Schaduwagent]   1. Herstart service 'esb-proxy'
[Schaduwagent]   2. Verhoog memory limit van 512MB naar 1024MB
[Schaduwagent]
[Schaduwagent] Wil je dat ik actie 1 uitvoer? [j/n]
> j
[Schaduwagent] Service 'esb-proxy' herstart... OK
[Schaduwagent] Health check... OK
[Schaduwagent] Zaaksysteem is weer bereikbaar.
```

**Deliverables Fase 0:**
- Werkend prototype: CLI tool die via SSH een werkstation diagnosticeert
- Claude als analyse-engine via Bedrock EU
- Container-geïsoleerde agent executie
- Basis logging van diagnose en acties
- Demo-klaar voor Marlies en beheersorganisatie

**Technologie:**
- Python + Anthropic Agent SDK (of TypeScript + NanoClaw-patroon)
- Docker voor container-isolatie
- SSH/WinRM voor werkstation-toegang
- Claude via AWS Bedrock EU (Frankfurt)

---

### Fase 1: Screen observatie toevoegen (2-3 weken)

**Toevoeging:** Naast OS-diagnose nu ook meekijken met het scherm.

- ScreenPipe installeren op werkstation (of simpeler: periodieke screenshots via SSH)
- Claude Vision voor interpretatie scherminhoud
- Correlatie: "Gebruiker ziet fout X" + "Systeem toont Y in logs"
- Nog steeds CLI-interface, maar nu met schermcontext

---

### Fase 2: Chat interface + TOPdesk (3-4 weken)

**Van CLI naar chat, en eerste integratie:**

- Chat widget (Chatwoot of simpele web UI) vervangt terminal
- Gebruiker kan zelf een melding doen via chat
- TOPdesk ticket automatisch aanmaken met diagnose-context
- Servicedeskmedewerker kan via dashboard meekijken

---

### Fase 3: CMDB & GGM + meerdere storingen (3-4 weken)

- CMDBuild koppeling voor IT-landschap awareness
- Vertaling technisch → begrijpelijk via GGM mapping
- Uitbreiding naar 5-10 storingstypen
- Impact-analyse: welke systemen/gebruikers geraakt?

---

### Fase 4: Geautomatiseerde remediatie (4-6 weken)

- Ansible AWX voor gecontroleerde acties
- Approval workflow: risicovolle acties vereisen menselijke goedkeuring
- Kennisbank: elke oplossing wordt vastgelegd
- Monitoring-integratie (Keep + Grafana)

---

### Fase 5: Opschalen & hardenen (doorlopend)

- Uitrol naar meer werkplekken
- Mistral als lokale fallback-LLM
- FSC-compliance voor gemeentelijk dataverkeer
- NL Design System voor chat widget
- Continue verbetering op basis van feedback
- Rapportage en dashboards voor beheersorganisatie

---

### Fasering visueel

```
Fase 0 (wk 1-3)     Fase 1 (wk 4-6)     Fase 2 (wk 7-10)
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ 1 SD-mw +    │     │ + Screen     │     │ + Chat UI    │
│ 1 werkstation│────►│   observatie │────►│ + TOPdesk    │
│ CLI + SSH    │     │ + Vision     │     │   integratie │
│ Claude EU    │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘

Fase 3 (wk 11-14)   Fase 4 (wk 15-20)   Fase 5 (doorlopend)
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ + CMDBuild   │     │ + Ansible    │     │ + Opschaling │
│ + GGM        │────►│   AWX        │────►│ + Mistral    │
│ + Meer       │     │ + Approval   │     │ + FSC        │
│   storingen  │     │ + Kennisbank │     │ + NL Design  │
└──────────────┘     └──────────────┘     └──────────────┘
```

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
| CMDB/GGM (vertaling technisch → begrijpelijk) | Levert de vertaallaag: technisch → begrijpelijk  |
| TOPdesk categorisering            | Schaduwagent levert de data voor betere categorisering        |
| Enthousiasme beheersorganisatie   | Schaduwagent is het meest zichtbare, tastbare resultaat       |
| BlueDolphin (optioneel)           | Bestaande EA-data kan als extra bron dienen via API-koppeling |

De vier ideeën vormen samen één geheel: de schaduwagent is het **platform**, CMDB/GGM is de **kennislaag**, en betere TOPdesk-categorisering is het **resultaat**. Alles open source, alles in de EU.
