# Lesgenerator v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Vervang DeepSeek door Mistral/Pixtral, maak foto's optioneel, voeg volwasseneneducatie toe als aparte sectie met leergang-structuur, verbeter prompts met SVG + hint/uitleg-patroon, en voeg Playwright-kwaliteitsgate toe.

**Architecture:** Vier fasen: (1) provider-migratie in generate-lesson.py + workflow, (2) prompt-bestanden per niveau/provider, (3) issue-templates + leergangen.yml config, (4) leergangen-sitestructuur met generator + zoekfunctie + homepage. Bestaande schoollessen blijven onaangeroerd.

**Tech Stack:** Python 3.12, GitHub Actions, Mistral API (magistral-medium-2509 + pixtral-large-2411), Anthropic API, Playwright (Node.js), vanilla HTML/CSS/JS (statische site)

---

## Betrokken bestanden

| Bestand | Actie | Beschrijving |
|---|---|---|
| `.github/scripts/generate-lesson.py` | Wijzigen | Provider-migratie, foto's optioneel, niveau-gebaseerde prompt-selectie |
| `.github/workflows/generate-lesson.yml` | Wijzigen | Labels, Mistral secret, Playwright-gate, extended output header |
| `.github/scripts/lesson-prompt.txt` | Wijzigen | Opdracht aanpassen voor tekst-first, SVG-instructies toevoegen |
| `.github/scripts/lesson-prompt-mistral.txt` | Al aangemaakt | Basis Mistral-prompt (al klaar) |
| `.github/scripts/lesson-prompt-claude-onderbouw.txt` | Nieuw | Claude prompt voor onderbouw |
| `.github/scripts/lesson-prompt-claude-bovenbouw.txt` | Nieuw | Claude prompt voor bovenbouw |
| `.github/scripts/lesson-prompt-claude-volwasseneneducatie.txt` | Nieuw | Claude prompt voor volwassenen |
| `.github/scripts/lesson-prompt-mistral-onderbouw.txt` | Nieuw | Mistral prompt voor onderbouw |
| `.github/scripts/lesson-prompt-mistral-bovenbouw.txt` | Nieuw | Mistral prompt voor bovenbouw |
| `.github/scripts/lesson-prompt-mistral-volwasseneneducatie.txt` | Nieuw | Mistral prompt voor volwassenen |
| `.github/scripts/generate-leergangen.py` | Nieuw | Generator voor leergang-indexpagina's + JSON-zoekindex |
| `.github/scripts/validate-lesson.js` | Nieuw | Playwright-validatiescript (hergebruikt vanuit C:/temp) |
| `.github/scripts/playwright.config.js` | Nieuw | Playwright-configuratie voor CI |
| `.github/ISSUE_TEMPLATE/nieuwe-les.yml` | Hernoemen → `middelbareschool-les.yml` | Niveau-dropdown uitbreiden, foto's optioneel |
| `.github/ISSUE_TEMPLATE/volwassen-educatie.yml` | Nieuw | Template voor volwasseneneducatie |
| `.github/ISSUE_TEMPLATE/nieuwe-leergang.yml` | Nieuw | Aanvraag nieuwe leergang |
| `.github/workflows/sync-leergangen.yml` | Nieuw | Sync leergangen.yml → issue template dropdown |
| `leergangen.yml` | Nieuw | Config: domeinen + leergangen (beheerd door Ralph) |
| `leergangen/index.html` | Nieuw | Overzichtspagina alle domeinen |
| `index.html` | Wijzigen | Homepage: 2 ingangen (schoollessen + leergangen) |
| `package.json` | Nieuw | Node dependencies voor Playwright in CI |

---

## Fase 1 — Provider-migratie: DeepSeek → Mistral + foto's optioneel

### Taak 1: PROVIDERS-config in generate-lesson.py vervangen

**Bestanden:**
- Wijzigen: `.github/scripts/generate-lesson.py:28-43`

- [ ] **Stap 1.1: Vervang de PROVIDERS dict**

Vervang het blok op regels 28-43:

```python
PROVIDERS = {
    "mistral": {
        "name": "Mistral",
        "api_url": "https://api.mistral.ai/v1/chat/completions",
        "model": "magistral-medium-2509",
        "max_tokens": 12000,
        "temperature": 0.2,
        "env_key": "MISTRAL_API_KEY",
    },
    "pixtral": {
        "name": "Pixtral",
        "api_url": "https://api.mistral.ai/v1/chat/completions",
        "model": "pixtral-large-2411",
        "max_tokens": 12000,
        "temperature": 0.3,
        "env_key": "MISTRAL_API_KEY",
    },
    "claude": {
        "name": "Claude",
        "api_url": "https://api.anthropic.com/v1/messages",
        "model": "auto",
        "model_preference": ["claude-sonnet"],
        "max_tokens": 12000,
        "env_key": "ANTHROPIC_API_KEY",
    },
}
```

- [ ] **Stap 1.2: Vervang get_provider() logica**

De huidige `get_provider()` geeft "claude" als standaard. Vervang zodat:
- `AI_PROVIDER=claude` → claude
- `AI_PROVIDER=pixtral` → pixtral
- alles anders (incl. leeg) → mistral (maar als foto's aanwezig en provider=mistral, switch naar pixtral)

```python
def get_provider(has_photos: bool = False) -> str:
    """Bepaal provider. Standaard: mistral. Met foto's → pixtral tenzij expliciet anders."""
    provider = os.environ.get("AI_PROVIDER", "mistral").strip().lower()
    if provider not in PROVIDERS:
        print(f"WAARSCHUWING: Onbekende provider '{provider}', gebruik mistral.")
        provider = "mistral"
    # Auto-upgrade naar pixtral als foto's aanwezig en provider=mistral
    if provider == "mistral" and has_photos:
        print("  Foto's aanwezig + provider=mistral → automatisch pixtral geselecteerd")
        provider = "pixtral"
    return provider
```

- [ ] **Stap 1.3: Commit**

```bash
git add .github/scripts/generate-lesson.py
git commit -m "feat: replace DeepSeek with Mistral/Pixtral providers"
```

---

### Taak 2: Foto's optioneel maken in generate-lesson.py

**Bestanden:**
- Wijzigen: `.github/scripts/generate-lesson.py:786-810` (main())

- [ ] **Stap 2.1: Verwijder de fatale foto-check (regel 789-792)**

Verwijder:
```python
    if not fotos:
        print("FOUT: Geen foto's gevonden in het issue.")
        print(f"  Volledige issue body:\n{issue_body}")
        sys.exit(1)
```

Vervang door:
```python
    if fotos:
        print(f"  Foto's: {len(fotos)} gevonden")
    else:
        print("  Geen foto's — les wordt op basis van tekstbeschrijving gemaakt")
```

- [ ] **Stap 2.2: Provider-aanroep aanpassen voor foto-detectie**

Zoek de regel `provider = get_provider()` in `main()` en vervang:
```python
    provider = get_provider(has_photos=bool(fotos))
    config = PROVIDERS[provider].copy()
```

- [ ] **Stap 2.3: user_context aanpassen voor beide scenario's**

Vervang het hele blok dat `user_context` opbouwt (regels ~823-849):

```python
    # Bouw gebruikerscontext op
    has_photos = bool(images)
    if has_photos:
        photo_instruction = f"Analyseer de {len(images)} bijgevoegde foto('s) en maak er een complete interactieve les van."
    else:
        photo_instruction = "Er zijn geen foto's bijgevoegd. Gebruik je eigen vakkennis en de onderstaande beschrijving als basis voor de les."

    user_context = f"""Maak een interactieve les met de volgende gegevens:

- Titel: {titel}
- Vak: {vak}
- Niveau: {niveau}
- Auteur (GitHub): {issue_author}
{f'- Weergavenaam: {friendly_name}' if friendly_name else ''}

{photo_instruction}
Onthoud: maak EIGEN voorbeelden, kopieer niet letterlijk.
"""
    if extra:
        user_context += f"\nExtra instructies van de aanvrager:\n{extra}\n"
```

- [ ] **Stap 2.4: Foto-download alleen als foto's aanwezig**

Zorg dat het download-blok al geconditioneerd is (het is al een loop over `fotos`, dus werkt al). Alleen logmelding aanpassen:

```python
    # Download foto's (alleen als aanwezig)
    images = []
    if fotos:
        print(f"Foto's downloaden ({len(fotos)} stuks)...")
        for i, url in enumerate(fotos):
            print(f"  [{i+1}/{len(fotos)}] {url[:80]}...")
            img_data, media_type = download_image(url)
            images.append({
                "data_b64": base64.b64encode(img_data).decode('utf-8'),
                "media_type": media_type,
            })
        print(f"  {len(images)} foto's gedownload.")
    else:
        print("  Geen foto's te downloaden — tekstgebaseerde les")
```

- [ ] **Stap 2.5: Commit**

```bash
git add .github/scripts/generate-lesson.py
git commit -m "feat: make photos optional in lesson generation"
```

---

### Taak 3: Mistral API-aanroep implementeren

**Bestanden:**
- Wijzigen: `.github/scripts/generate-lesson.py` — nieuwe functie `call_mistral_api()`

- [ ] **Stap 3.1: Voeg call_mistral_api() toe**

Voeg toe na `call_deepseek_api()` (of vervang die):

```python
def call_mistral_api(api_key: str, images: list[dict], prompt_text: str, user_context: str, model: str = "") -> tuple[str, dict]:
    """Roep de Mistral API aan (OpenAI-compatibel). Ondersteunt vision via pixtral."""
    config = PROVIDERS.get("pixtral") if images else PROVIDERS.get("mistral")
    model = model or config["model"]

    # Bouw user message content op
    content = []
    for img in images:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{img['media_type']};base64,{img['data_b64']}"
            }
        })
    content.append({"type": "text", "text": user_context})

    payload = {
        "model": model,
        "max_tokens": config["max_tokens"],
        "temperature": config.get("temperature", 0.2),
        "messages": [
            {"role": "system", "content": prompt_text},
            {"role": "user", "content": content if images else user_context}
        ]
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        config["api_url"],
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else 'Geen details'
        print(f"Mistral API fout ({e.code}): {error_body}")
        sys.exit(1)

    # Mistral reasoning models retourneren soms een lijst van chunks
    msg = result["choices"][0]["message"]["content"]
    if isinstance(msg, list):
        response_text = " ".join(item["text"] for item in msg if item.get("type") == "text")
    else:
        response_text = msg

    usage = result.get("usage", {})
    log_entry = {
        "provider": "mistral",
        "model": model,
        "input_tokens": usage.get("prompt_tokens", 0),
        "output_tokens": usage.get("completion_tokens", 0),
    }
    return response_text, log_entry
```

- [ ] **Stap 3.2: Voeg anthropic-beta header toe aan call_claude_api()**

Zoek de headers in `call_claude_api()` en voeg toe:
```python
headers={
    'Content-Type': 'application/json',
    'x-api-key': api_key,
    'anthropic-version': '2023-06-01',
    'anthropic-beta': 'output-128k-2025-02-19',  # Extended output (tot 64k tokens)
},
```

Pas ook `max_tokens` aan naar 12000 in de PROVIDERS config (al gedaan in taak 1).

- [ ] **Stap 3.3: Registreer mistral/pixtral in call_ai_api()**

Vervang de dispatch-functie:
```python
def call_ai_api(provider: str, api_key: str, images: list[dict], prompt_text: str, user_context: str, model: str = "") -> tuple[str, dict]:
    if provider in ("mistral", "pixtral"):
        return call_mistral_api(api_key, images, prompt_text, user_context, model)
    elif provider == "claude":
        return call_claude_api(api_key, images, prompt_text, user_context, model)
    else:
        print(f"FOUT: Onbekende provider '{provider}'")
        sys.exit(1)
```

- [ ] **Stap 3.4: Commit**

```bash
git add .github/scripts/generate-lesson.py
git commit -m "feat: implement Mistral/Pixtral API integration"
```

---

### Taak 4: Workflow aanpassen (labels + secret + extended output)

**Bestanden:**
- Wijzigen: `.github/workflows/generate-lesson.yml`

- [ ] **Stap 4.1: Label-detectie aanpassen**

Vervang het label-filter bovenaan de workflow:
```yaml
    if: >
      (github.event_name == 'issues' && (github.event.label.name == 'nieuwe-les' || github.event.label.name == 'claude-les')) ||
      github.event_name == 'schedule' ||
      github.event_name == 'workflow_dispatch'
```

- [ ] **Stap 4.2: Provider-detectie in workflow aanpassen**

Vervang het blok dat `HAS_DEEPSEEK` bepaalt:
```bash
            HAS_CLAUDE=$(gh issue view "$ISSUE_NUM" --json labels --jq '.labels[].name' | grep -c '^claude-les$' || true)
            if [ "$HAS_CLAUDE" -gt 0 ]; then
              export AI_PROVIDER="claude"
            else
              export AI_PROVIDER="mistral"  # Mistral is standaard; auto-upgrade naar pixtral als foto's aanwezig
            fi
```

- [ ] **Stap 4.3: MISTRAL_API_KEY toevoegen aan workflow env**

```yaml
        env:
          MISTRAL_API_KEY: ${{ secrets.MISTRAL_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
```

- [ ] **Stap 4.4: Label-filter voor cron bijwerken**

In de cron-stap die issues ophaalt, de deepseek-les label vervangen door claude-les:
```bash
            ISSUES_CLAUDE=$(gh issue list \
              --label "claude-les" \
              --state open \
              --json number,labels \
              --jq '[.[] | select(.labels | map(.name) | index("verwerkt") | not)] | .[].number' \
              | tr '\n' ' ')
            ISSUES_MISTRAL=$(gh issue list \
              --label "nieuwe-les" \
              --state open \
              --json number,labels \
              --jq '[.[] | select(.labels | map(.name) | index("verwerkt") | not)] | .[].number' \
              | tr '\n' ' ')
            echo "issue_numbers=${ISSUES_CLAUDE}${ISSUES_MISTRAL}" >> "$GITHUB_OUTPUT"
```

- [ ] **Stap 4.5: MISTRAL_API_KEY toevoegen als GitHub Secret**

Voer uit in browser: github.com → repo → Settings → Secrets → Actions → New secret
- Name: `MISTRAL_API_KEY`
- Value: `veOcILfoIXe8srnaUeSCM4UzqkegtmCt` *(vervang door nieuwe sleutel na rotatie)*

- [ ] **Stap 4.6: Commit**

```bash
git add .github/workflows/generate-lesson.yml
git commit -m "feat: migrate workflow from DeepSeek to Mistral labels and secrets"
```

---

## Fase 2 — Prompt-bestanden per niveau en provider

### Taak 5: Niveau-gebaseerde prompt-selectie in generate-lesson.py

**Bestanden:**
- Wijzigen: `.github/scripts/generate-lesson.py:811-821`

- [ ] **Stap 5.1: Prompt-selectie aanpassen naar provider+niveau**

Vervang het prompt-laadblok:
```python
    # Lees de prompt template — provider + niveau specifiek
    script_dir = Path(__file__).parent

    # Normaliseer niveau naar slug
    niveau_slug = niveau.lower().replace(' ', '-').replace('/', '-')
    # Mapping van niveau-display naar slug
    niveau_map = {
        'onderbouw': 'onderbouw',
        'havo bovenbouw': 'bovenbouw',
        'vwo bovenbouw': 'bovenbouw',
        'mbo': 'bovenbouw',       # MBO gebruikt bovenbouw-prompt
        'volwasseneneducatie': 'volwasseneneducatie',
    }
    niveau_slug = niveau_map.get(niveau.lower(), 'bovenbouw')

    # Zoek prompt: 1) provider+niveau, 2) provider, 3) generiek
    candidates = [
        script_dir / f'lesson-prompt-{provider}-{niveau_slug}.txt',
        script_dir / f'lesson-prompt-{provider}.txt',
        script_dir / 'lesson-prompt.txt',
    ]
    prompt_path = next((p for p in candidates if p.exists()), candidates[-1])
    prompt_text = prompt_path.read_text(encoding='utf-8')
    print(f"  Prompt: {prompt_path.name}")
```

- [ ] **Stap 5.2: Commit**

```bash
git add .github/scripts/generate-lesson.py
git commit -m "feat: select prompt by provider + niveau"
```

---

### Taak 6: Zes prompt-bestanden aanmaken

**Bestanden:**
- Nieuw: `.github/scripts/lesson-prompt-claude-onderbouw.txt`
- Nieuw: `.github/scripts/lesson-prompt-claude-bovenbouw.txt`
- Nieuw: `.github/scripts/lesson-prompt-claude-volwasseneneducatie.txt`
- Nieuw: `.github/scripts/lesson-prompt-mistral-onderbouw.txt`
- Nieuw: `.github/scripts/lesson-prompt-mistral-bovenbouw.txt`
- Nieuw: `.github/scripts/lesson-prompt-mistral-volwasseneneducatie.txt`

- [ ] **Stap 6.1: Maak lesson-prompt-claude-onderbouw.txt**

Inhoud: kopieer `lesson-prompt.txt`, vervang de taal-sectie:
```
## Taal en doelgroep
- Doelgroep: leerlingen 12-14 jaar (klas 1-3)
- Schrijf op B1-niveau: korte zinnen, concrete voorbeelden
- Vermijd jargon tenzij je het direct uitlegt
- Spreek de leerling aan met "je/jij"
- Gebruik voorbeelden uit de belevingswereld van jongeren (sport, games, social media)
```

En voeg SVG-vereiste toe in "Verplichte componenten":
```
5b. **Minimaal 1 inline SVG-diagram** dat een begrip visueel verduidelijkt
```

En voeg het hint/uitleg-patroon toe (identiek aan lesson-prompt-mistral.txt, sectie "JavaScript-patroon voor oefeningen").

- [ ] **Stap 6.2: Maak lesson-prompt-claude-bovenbouw.txt**

Gelijk aan onderbouw-prompt maar doelgroep:
```
## Taal en doelgroep
- Doelgroep: leerlingen 15-18 jaar (HAVO/VWO bovenbouw, MBO)
- Schrijf op B2-niveau: formele termen mogen, maar leg ze uit
- Spreek de leerling aan met "je/jij"
- Oefeningen mogen complexer zijn: meerstaps, combinatievraagstukken
```

- [ ] **Stap 6.3: Maak lesson-prompt-claude-volwasseneneducatie.txt**

Doelgroep en toon anders:
```
## Taal en doelgroep
- Doelgroep: volwassen professionals
- Spreek de cursist aan met "je"
- Vaktermen mogen verondersteld worden bij de doelgroep, maar leg nieuwe termen wel uit
- Zakelijke, directe toon — geen schoolse scaffolding
- Gebruik praktijkscenario's en herkenbare werksituaties als voorbeelden
- Geen "ik doe voor — wij doen samen" structuur; direct naar toepasbare kennis

## Visuele weergave (extra belangrijk voor volwassenenonderwijs)
Droge theorie over technische onderwerpen wordt aanzienlijk beter met schema's. Verplicht:
- **Minimaal 2 inline SVG-diagrammen** (netwerktopologie, OSI-lagen, procesflow, etc.)
- Gebruik de SVG-sjablonen uit de sectie hieronder als basis
```

Voeg dezelfde SVG-sjablonen toe als in lesson-prompt-mistral.txt.

- [ ] **Stap 6.4: Maak lesson-prompt-mistral-onderbouw.txt, -bovenbouw.txt, -volwasseneneducatie.txt**

Gebruik `lesson-prompt-mistral.txt` als basis. Pas per variant alleen de "Taal en doelgroep" sectie aan (zelfde inhoud als de Claude-varianten hierboven). De redeneer-instructies, SVG-sjablonen en hint/uitleg-patronen blijven identiek.

- [ ] **Stap 6.5: Verwijder lesson-prompt-deepseek.txt**

```bash
git rm .github/scripts/lesson-prompt-deepseek.txt
```

- [ ] **Stap 6.6: Commit**

```bash
git add .github/scripts/
git commit -m "feat: add 6 level/provider-specific prompt files, remove deepseek prompt"
```

---

## Fase 3 — Issue-templates + leergangen.yml

### Taak 7: Issue-template voor middelbareschool hernoemen en bijwerken

**Bestanden:**
- Hernoemen: `.github/ISSUE_TEMPLATE/nieuwe-les.yml` → `middelbareschool-les.yml`
- Wijzigen: `.github/ISSUE_TEMPLATE/middelbareschool-les.yml`

- [ ] **Stap 7.1: Hernoem bestand**

```bash
git mv .github/ISSUE_TEMPLATE/nieuwe-les.yml .github/ISSUE_TEMPLATE/middelbareschool-les.yml
```

- [ ] **Stap 7.2: Pas inhoud aan**

Vervang de volledige inhoud van `middelbareschool-les.yml`:

```yaml
name: "📚 Middelbare school — nieuwe les"
description: Beschrijf het onderwerp of upload foto's van lesmateriaal, en er wordt automatisch een interactieve les van gemaakt
title: "[Les] wordt automatisch ingevuld"
labels: ["nieuwe-les"]
body:
  - type: markdown
    attributes:
      value: |
        ## Nieuwe les aanvragen
        Beschrijf het onderwerp dat je wilt leren, of upload foto's van lesmateriaal (bijv. een lesboekpagina of werkblad).
        Beide werken — een goede omschrijving is even waardevol als foto's.

        > **Tip:** De titel hierboven wordt automatisch bijgewerkt na het indienen.

  - type: input
    id: naam
    attributes:
      label: Je naam (wordt getoond op de site)
      description: Hoe wil je genoemd worden bij je lessen?
      placeholder: "bijv. Ralph W."
    validations:
      required: false

  - type: input
    id: titel
    attributes:
      label: Titel van de les
      description: Geef een korte, beschrijvende titel
      placeholder: "bijv. Kwadratische functies"
    validations:
      required: true

  - type: dropdown
    id: vak
    attributes:
      label: Vak
      options:
        - Wiskunde
        - Scheikunde
        - Biologie
        - Natuurkunde
        - Maatschappijleer
        - Geschiedenis
        - Aardrijkskunde
        - Economie
        - Nederlands
        - Engels
        - Anders
    validations:
      required: true

  - type: input
    id: vak_anders
    attributes:
      label: Ander vak (alleen invullen als je "Anders" koos)
      placeholder: "bijv. Filosofie"

  - type: dropdown
    id: niveau
    attributes:
      label: Niveau
      options:
        - Onderbouw (klas 1-3)
        - HAVO bovenbouw
        - VWO bovenbouw
        - MBO
    validations:
      required: true

  - type: textarea
    id: fotos
    attributes:
      label: "Foto's van lesmateriaal (optioneel)"
      description: |
        Sleep hier foto's naartoe of plak ze in dit veld — bijv. van een lesboekpagina, werkblad of aantekeningen.
        Ondersteunde formaten: PNG, JPG, GIF, WEBP.
        Geen foto's? Dat is prima — gebruik dan het omschrijvingsveld hieronder.
      placeholder: "Sleep foto's hierheen of plak ze... (optioneel)"
    validations:
      required: false

  - type: textarea
    id: extra
    attributes:
      label: Omschrijving / extra instructies
      description: |
        Beschrijf het onderwerp, de doelgroep, wat je wilt oefenen of welke stof behandeld moet worden.
        Hoe meer detail, hoe beter de les. Bij foto's: geef aan welke delen je wilt behandelen.
      placeholder: "bijv. Behandel enkelvoudige en samengestelde kansen, boomdiagrammen en de optellingsregel"
    validations:
      required: false
```

- [ ] **Stap 7.3: Commit**

```bash
git add .github/ISSUE_TEMPLATE/
git commit -m "feat: rename and update middelbareschool-les template, photos optional"
```

---

### Taak 8: leergangen.yml aanmaken

**Bestanden:**
- Nieuw: `leergangen.yml`

- [ ] **Stap 8.1: Maak leergangen.yml aan**

```yaml
# Leergang-structuur voor volwasseneneducatie
# Beheerd door Ralph Wagter
# Na wijziging: workflow sync-leergangen.yml werkt automatisch de issue-template bij

domeinen:
  - naam: ICT
    slug: ict
    leergangen:
      - naam: ICT Basis
        slug: ict-basis
        omschrijving: Fundamentele ICT-kennis voor beginners
      - naam: Vibecoding
        slug: vibecoding
        omschrijving: Vibe-based software development met AI-tools

  - naam: Cyber
    slug: cyber
    leergangen:
      - naam: Netwerken en Protocollen
        slug: netwerken-en-protocollen
        omschrijving: TCP/IP, UDP, poorten, subnetting en firewalling
      - naam: Blue Team Basics
        slug: blue-team-basics
        omschrijving: Verdediging, SIEM, log-analyse en incidentrespons

  - naam: Veranderkunde
    slug: veranderkunde
    leergangen:
      - naam: Methodes
        slug: methodes
        omschrijving: Veranderkundige methodes en modellen
```

- [ ] **Stap 8.2: Commit**

```bash
git add leergangen.yml
git commit -m "feat: add leergangen.yml config with initial domains and courses"
```

---

### Taak 9: Issue-template voor volwassen-educatie

**Bestanden:**
- Nieuw: `.github/ISSUE_TEMPLATE/volwassen-educatie.yml`

- [ ] **Stap 9.1: Maak volwassen-educatie.yml aan**

```yaml
name: "🎓 Volwasseneneducatie — nieuwe les"
description: Beschrijf het onderwerp voor een leergang en er wordt automatisch een interactieve les van gemaakt
title: "[Leergang] wordt automatisch ingevuld"
labels: ["nieuwe-les", "volwasseneneducatie"]
body:
  - type: markdown
    attributes:
      value: |
        ## Nieuwe les voor een leergang aanvragen
        Beschrijf het onderwerp dat je wilt behandelen. Foto's zijn optioneel.
        De les wordt geplaatst in de leergang-structuur onder het gekozen domein.

  - type: input
    id: naam
    attributes:
      label: Je naam (verschijnt in de colofon van de les)
      placeholder: "bijv. Jan de Vries"
    validations:
      required: true

  - type: input
    id: titel
    attributes:
      label: Titel van de les
      placeholder: "bijv. Subnetting berekenen"
    validations:
      required: true

  - type: dropdown
    id: domein
    attributes:
      label: Domein
      description: Kies het domein. Staat jouw domein er niet bij? Vraag een nieuwe leergang aan via het aparte template.
      options:
        - ICT
        - Cyber
        - Veranderkunde
    validations:
      required: true

  - type: dropdown
    id: leergang
    attributes:
      label: Leergang
      description: Kies de leergang. De opties hieronder bevatten alle bestaande leergangen — kies de juiste bij jouw domein.
      options:
        - ICT > ICT Basis
        - ICT > Vibecoding
        - Cyber > Netwerken en Protocollen
        - Cyber > Blue Team Basics
        - Veranderkunde > Methodes
    validations:
      required: true

  - type: textarea
    id: fotos
    attributes:
      label: "Foto's of lesmateriaal (optioneel)"
      description: Sleep hier foto's naartoe of plak ze. Zonder foto's wordt de omschrijving als basis gebruikt.
      placeholder: "Sleep foto's hierheen of plak ze..."
    validations:
      required: false

  - type: textarea
    id: extra
    attributes:
      label: Omschrijving / lesinhoud
      description: Beschrijf het onderwerp, de doelgroep en wat je wilt behandelen. Hoe meer detail, hoe beter de les.
      placeholder: "bijv. Uitleg van subnetting: CIDR-notatie, subnet masks berekenen, /24 en /16 netwerken opdelen"
    validations:
      required: true
```

- [ ] **Stap 9.2: Commit**

```bash
git add .github/ISSUE_TEMPLATE/volwassen-educatie.yml
git commit -m "feat: add volwassen-educatie issue template"
```

---

### Taak 10: Template voor nieuwe leergang aanvragen

**Bestanden:**
- Nieuw: `.github/ISSUE_TEMPLATE/nieuwe-leergang.yml`

- [ ] **Stap 10.1: Maak nieuwe-leergang.yml aan**

```yaml
name: "📂 Nieuwe leergang aanvragen"
description: Vraag een nieuw domein of leergang aan voor de volwasseneneducatie-sectie
title: "[Leergang aanvraag] "
labels: ["leergang-aanvraag"]
body:
  - type: markdown
    attributes:
      value: |
        ## Nieuwe leergang aanvragen
        Een leergang aanvragen is een handmatig proces. Na goedkeuring wordt de leergang toegevoegd aan `leergangen.yml` en is die beschikbaar in het volwassen-educatie formulier.

  - type: input
    id: naam
    attributes:
      label: Jouw naam
      placeholder: "bijv. Ralph Wagter"
    validations:
      required: true

  - type: input
    id: domein
    attributes:
      label: Domein (nieuw of bestaand)
      placeholder: "bijv. Data & Analyse"
    validations:
      required: true

  - type: input
    id: leergang
    attributes:
      label: Naam van de leergang
      placeholder: "bijv. Python voor data-analyse"
    validations:
      required: true

  - type: textarea
    id: omschrijving
    attributes:
      label: Omschrijving
      description: Wat behandelt deze leergang? Voor wie is het bedoeld?
      placeholder: "bijv. Python-basis voor analisten zonder programmeerervaring: DataFrames, visualisatie, eenvoudige ML"
    validations:
      required: true
```

- [ ] **Stap 10.2: Commit**

```bash
git add .github/ISSUE_TEMPLATE/nieuwe-leergang.yml
git commit -m "feat: add nieuwe-leergang request template"
```

---

### Taak 11: Workflow voor auto-sync leergangen.yml → issue template

**Bestanden:**
- Nieuw: `.github/workflows/sync-leergangen.yml`

- [ ] **Stap 11.1: Maak sync-leergangen.yml aan**

```yaml
name: Sync leergangen naar issue template

on:
  push:
    paths:
      - 'leergangen.yml'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Python opzetten
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Sync leergangen naar issue template
        run: |
          python3 << 'PYEOF'
          import yaml, re
          from pathlib import Path

          config = yaml.safe_load(Path('leergangen.yml').read_text())

          # Bouw opties lijst: "Domein > Leergang"
          opties = []
          domeinen_opties = []
          for domein in config['domeinen']:
              domeinen_opties.append(domein['naam'])
              for lg in domein['leergangen']:
                  opties.append(f"{domein['naam']} > {lg['naam']}")

          # Update domein-opties in template
          template_path = Path('.github/ISSUE_TEMPLATE/volwassen-educatie.yml')
          content = template_path.read_text()

          # Vervang domein opties
          domein_block = '      options:\n' + ''.join(f'        - {d}\n' for d in domeinen_opties)
          content = re.sub(
              r'(id: domein.*?options:\n)(.*?)(^\s{4}-)',
              lambda m: m.group(1) + domein_block + m.group(3) if False else m.group(0),
              content, flags=re.DOTALL
          )

          # Simpelere aanpak: vervang options blokken met markers
          lines = content.split('\n')
          new_lines = []
          in_domein_options = False
          in_leergang_options = False
          for line in lines:
              if '# DOMEIN_OPTIONS_START' in line:
                  in_domein_options = True
                  new_lines.append(line)
                  for d in domeinen_opties:
                      new_lines.append(f'        - {d}')
                  continue
              if '# DOMEIN_OPTIONS_END' in line:
                  in_domein_options = False
              if '# LEERGANG_OPTIONS_START' in line:
                  in_leergang_options = True
                  new_lines.append(line)
                  for opt in opties:
                      new_lines.append(f'        - {opt}')
                  continue
              if '# LEERGANG_OPTIONS_END' in line:
                  in_leergang_options = False
              if not in_domein_options and not in_leergang_options:
                  new_lines.append(line)

          template_path.write_text('\n'.join(new_lines))
          print(f"Gesynchroniseerd: {len(domeinen_opties)} domeinen, {len(opties)} leergangen")
          PYEOF

      - name: Installeer PyYAML
        run: pip install pyyaml

      - name: Commit als gewijzigd
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .github/ISSUE_TEMPLATE/volwassen-educatie.yml
          git diff --cached --quiet || git commit -m "sync: leergangen.yml → issue template dropdowns"
          git push
```

> **Opmerking:** Voeg `# DOMEIN_OPTIONS_START` / `# DOMEIN_OPTIONS_END` en `# LEERGANG_OPTIONS_START` / `# LEERGANG_OPTIONS_END` markers toe aan de volwassen-educatie.yml template (taak 9). De sync-workflow gebruikt deze markers.

- [ ] **Stap 11.2: Voeg markers toe aan volwassen-educatie.yml**

In `.github/ISSUE_TEMPLATE/volwassen-educatie.yml`, voeg commentaar-markers toe rond de options-blokken:
```yaml
      options: # DOMEIN_OPTIONS_START
        - ICT
        - Cyber
        - Veranderkunde
        # DOMEIN_OPTIONS_END
```

en:
```yaml
      options: # LEERGANG_OPTIONS_START
        - ICT > ICT Basis
        ...
        # LEERGANG_OPTIONS_END
```

- [ ] **Stap 11.3: Commit**

```bash
git add .github/workflows/sync-leergangen.yml .github/ISSUE_TEMPLATE/volwassen-educatie.yml
git commit -m "feat: add auto-sync workflow for leergangen.yml to issue template"
```

---

### Taak 12: generate-lesson.py uitbreiden voor leergang-routing

**Bestanden:**
- Wijzigen: `.github/scripts/generate-lesson.py` — parse_issue_body() en save-logica

- [ ] **Stap 12.1: parse_issue_body() uitbreiden voor leergang-velden**

Voeg toe aan de parse-functie (na de bestaande velden):
```python
    result["domein"] = ""
    result["leergang"] = ""
    # ...in de header-parsing loop:
    elif 'domein' in header:
        current_field = 'domein'
    elif 'leergang' in header:
        current_field = 'leergang'
```

- [ ] **Stap 12.2: Leergang-routing in het opslagpad**

Zoek de code die `output_path` bepaalt in `main()`. Voeg toe:
```python
    domein = parsed.get('domein', '').strip()
    leergang = parsed.get('leergang', '').strip()

    # Verwijder "Domein > " prefix als aanwezig (uit leergang-dropdown)
    if ' > ' in leergang:
        domein_prefix, leergang = leergang.split(' > ', 1)
        if not domein:
            domein = domein_prefix

    # Bepaal opslagpad
    if domein and leergang:
        # Volwasseneneducatie: /leergangen/{domein-slug}/{leergang-slug}/{les-slug}/
        domein_slug = domein.lower().replace(' ', '-')
        leergang_slug = leergang.lower().replace(' ', '-')
        base_dir = Path('leergangen') / domein_slug / leergang_slug / les_slug
    else:
        # Schoolles: /{auteur}/{vak}/{niveau}/{les-slug}/
        base_dir = Path(issue_author) / vak_slug / niveau_slug / les_slug
```

- [ ] **Stap 12.3: Commit**

```bash
git add .github/scripts/generate-lesson.py
git commit -m "feat: route volwasseneneducatie lessons to leergangen/ path"
```

---

## Fase 4 — Leergangen-sitestructuur

### Taak 13: Generator voor leergang-indexpagina's

**Bestanden:**
- Nieuw: `.github/scripts/generate-leergangen.py`

- [ ] **Stap 13.1: Maak generate-leergangen.py**

```python
#!/usr/bin/env python3
"""
Genereert indexpagina's voor de leergangen-sectie en een JSON-zoekindex.

Structuur:
  leergangen/index.html              — overzicht alle domeinen
  leergangen/{domein}/index.html     — overzicht leergangen in domein
  leergangen/{domein}/{leergang}/index.html — lessen in leergang
  leergangen/search-index.json       — zoekindex voor client-side search
"""

import json
import yaml
from pathlib import Path
from datetime import datetime

HOME_URL = "https://rwrw01.github.io/Claudecodedingetjes"

def slugify(naam: str) -> str:
    return naam.lower().replace(' ', '-').replace('/', '-').replace('>', '-')

def lees_metadata(les_dir: Path) -> dict:
    meta_file = les_dir / 'metadata.json'
    if meta_file.exists():
        return json.loads(meta_file.read_text(encoding='utf-8'))
    return {}

def genereer_domein_index(domein: dict, base_path: Path):
    domein_slug = domein['slug']
    domein_pad = base_path / domein_slug
    domein_pad.mkdir(parents=True, exist_ok=True)

    kaarten = []
    for lg in domein['leergangen']:
        lg_slug = lg['slug']
        kaarten.append(f"""
        <a class="card" href="{lg_slug}/">
            <h3>{lg['naam']}</h3>
            <p class="muted">{lg.get('omschrijving', '')}</p>
        </a>""")

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{domein['naam']} — Leergangen</title>
    {_style()}
</head>
<body>
    <header style="background:linear-gradient(135deg,#1e293b,#334155);color:white;padding:2.5rem 1rem;text-align:center;">
        <h1>{domein['naam']}</h1>
        <p style="opacity:.8">Leergangen</p>
    </header>
    <nav class="breadcrumb">
        <a href="{HOME_URL}">Home</a> &rsaquo;
        <a href="../">Leergangen</a> &rsaquo;
        {domein['naam']}
    </nav>
    <div class="container">
        {''.join(kaarten)}
    </div>
    {_footer()}
</body>
</html>"""
    (domein_pad / 'index.html').write_text(html, encoding='utf-8')
    print(f"  {domein_pad}/index.html")

def genereer_leergang_index(domein: dict, leergang: dict, base_path: Path):
    domein_slug = domein['slug']
    lg_slug = leergang['slug']
    lg_pad = base_path / domein_slug / lg_slug
    lg_pad.mkdir(parents=True, exist_ok=True)

    # Zoek lessen: alfabetisch op titel
    les_dirs = sorted(
        [d for d in lg_pad.iterdir() if d.is_dir() and (d / 'index.html').exists()],
        key=lambda d: (lees_metadata(d).get('titel', d.name) or d.name).lower()
    )

    kaarten = []
    for les_dir in les_dirs:
        meta = lees_metadata(les_dir)
        titel = meta.get('titel', les_dir.name.replace('-', ' ').title())
        auteur = meta.get('friendly_name') or meta.get('issue_author', '')
        kaarten.append(f"""
        <a class="card" href="{les_dir.name}/">
            <h3>{titel}</h3>
            {f'<p class="muted">door {auteur}</p>' if auteur else ''}
        </a>""")

    if not kaarten:
        kaarten = ['<p class="muted">Nog geen lessen in deze leergang.</p>']

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{leergang['naam']} — {domein['naam']}</title>
    {_style()}
</head>
<body>
    <header style="background:linear-gradient(135deg,#3730a3,#6366f1);color:white;padding:2.5rem 1rem;text-align:center;">
        <h1>{leergang['naam']}</h1>
        <p style="opacity:.8">{leergang.get('omschrijving', '')}</p>
    </header>
    <nav class="breadcrumb">
        <a href="{HOME_URL}">Home</a> &rsaquo;
        <a href="../../">Leergangen</a> &rsaquo;
        <a href="../">{domein['naam']}</a> &rsaquo;
        {leergang['naam']}
    </nav>
    <div class="container">
        <div class="search-box">
            <input type="text" id="zoek" placeholder="Zoek in deze leergang..." oninput="zoek(this.value)">
        </div>
        <div id="lessen">{''.join(kaarten)}</div>
    </div>
    {_footer()}
    <script>
    function zoek(q) {{
        q = q.toLowerCase();
        document.querySelectorAll('#lessen .card').forEach(card => {{
            card.style.display = card.textContent.toLowerCase().includes(q) ? '' : 'none';
        }});
    }}
    </script>
</body>
</html>"""
    (lg_pad / 'index.html').write_text(html, encoding='utf-8')
    print(f"  {lg_pad}/index.html")

def genereer_hoofdindex(config: dict, base_path: Path):
    domein_kaarten = []
    for domein in config['domeinen']:
        n_leergangen = len(domein['leergangen'])
        domein_kaarten.append(f"""
        <a class="card" href="{domein['slug']}/">
            <h3>{domein['naam']}</h3>
            <p class="muted">{n_leergangen} leergang{'en' if n_leergangen != 1 else ''}</p>
        </a>""")

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leergangen — Volwasseneneducatie</title>
    {_style()}
</head>
<body>
    <header style="background:linear-gradient(135deg,#1e293b,#334155);color:white;padding:3rem 1rem;text-align:center;">
        <h1>Leergangen</h1>
        <p style="opacity:.8">Interactieve lessen voor volwasseneneducatie</p>
    </header>
    <nav class="breadcrumb">
        <a href="{HOME_URL}">Home</a> &rsaquo; Leergangen
    </nav>
    <div class="container">
        <div class="search-box">
            <input type="text" id="zoek" placeholder="Zoek door alle leergangen..." oninput="zoekGlobaal(this.value)">
        </div>
        <div id="resultaten" style="display:none"></div>
        <div id="domeinen">{''.join(domein_kaarten)}</div>
    </div>
    {_footer()}
    <script>
    let searchIndex = null;
    async function laadIndex() {{
        const r = await fetch('search-index.json');
        searchIndex = await r.json();
    }}
    laadIndex();
    function zoekGlobaal(q) {{
        if (!q) {{ document.getElementById('domeinen').style.display=''; document.getElementById('resultaten').style.display='none'; return; }}
        document.getElementById('domeinen').style.display='none';
        const res = document.getElementById('resultaten');
        res.style.display='';
        if (!searchIndex) {{ res.innerHTML='<p>Zoekindex laden...</p>'; return; }}
        const hits = searchIndex.filter(l => (l.titel+' '+l.leergang+' '+l.domein+' '+l.omschrijving).toLowerCase().includes(q.toLowerCase()));
        res.innerHTML = hits.length
            ? hits.map(h => `<a class="card" href="${{HOME_URL}}/${{h.pad}}"><h3>${{h.titel}}</h3><p class="muted">${{h.domein}} &rsaquo; ${{h.leergang}}</p></a>`).join('')
            : '<p class="muted">Geen resultaten gevonden.</p>';
    }}
    </script>
</body>
</html>"""
    (base_path / 'index.html').write_text(html, encoding='utf-8')
    print(f"  {base_path}/index.html")

def genereer_search_index(config: dict, base_path: Path):
    entries = []
    for domein in config['domeinen']:
        for lg in domein['leergangen']:
            lg_pad = base_path / domein['slug'] / lg['slug']
            if not lg_pad.exists():
                continue
            for les_dir in lg_pad.iterdir():
                if not les_dir.is_dir():
                    continue
                meta = lees_metadata(les_dir)
                if not meta:
                    continue
                entries.append({
                    "titel": meta.get('titel', les_dir.name),
                    "domein": domein['naam'],
                    "leergang": lg['naam'],
                    "omschrijving": meta.get('extra', ''),
                    "auteur": meta.get('friendly_name') or meta.get('issue_author', ''),
                    "pad": str(les_dir.relative_to(Path('.'))).replace('\\', '/') + '/index.html',
                })
    (base_path / 'search-index.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"  {base_path}/search-index.json ({len(entries)} lessen geïndexeerd)")

def _style() -> str:
    return """<style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Segoe UI',system-ui,sans-serif;background:#f8fafc;color:#1e293b;line-height:1.6}
        .container{max-width:800px;margin:0 auto;padding:2rem 1rem}
        .card{display:block;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1rem;text-decoration:none;color:#1e293b;transition:transform .15s,box-shadow .15s}
        .card:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(0,0,0,.1)}
        .card h3{margin-bottom:.25rem}
        .muted{color:#64748b;font-size:.9rem}
        .breadcrumb{max-width:800px;margin:.75rem auto;padding:0 1rem;font-size:.85rem;color:#64748b}
        .breadcrumb a{color:#2563eb;text-decoration:none}
        .search-box{margin-bottom:1.5rem}
        .search-box input{width:100%;padding:.75rem 1rem;border:1px solid #e2e8f0;border-radius:8px;font-size:1rem;outline:none}
        .search-box input:focus{border-color:#2563eb;box-shadow:0 0 0 3px #dbeafe}
    </style>"""

def _footer() -> str:
    return """<footer style="text-align:center;padding:2rem 1rem;color:#64748b;font-size:.85rem;border-top:1px solid #e2e8f0;margin-top:2rem;">
        Gemaakt door Ralph Wagter met <a href="https://claude.ai" style="color:#2563eb;">Claude Code</a>.
        Vrij hergebruik onder <a href="https://eupl.eu/" style="color:#2563eb;">EUPL-1.2</a>.
        <a href="https://github.com/rwrw01/Claudecodedingetjes" style="color:#2563eb;">GitHub</a>
    </footer>"""

def main():
    config = yaml.safe_load(Path('leergangen.yml').read_text(encoding='utf-8'))
    base_path = Path('leergangen')
    base_path.mkdir(exist_ok=True)

    print("Genereer leergang-indexpagina's...")
    genereer_hoofdindex(config, base_path)
    for domein in config['domeinen']:
        genereer_domein_index(domein, base_path)
        for leergang in domein['leergangen']:
            genereer_leergang_index(domein, leergang, base_path)
    genereer_search_index(config, base_path)
    print("Klaar.")

if __name__ == '__main__':
    main()
```

- [ ] **Stap 13.2: Voeg `pyyaml` toe aan de GitHub Actions stap**

In `.github/workflows/generate-lesson.yml`, voeg `pyyaml` toe aan de pip-install stap:
```bash
pip install Pillow pyyaml
```

- [ ] **Stap 13.3: Roep generate-leergangen.py aan na elke leergang-les**

In `generate-lesson.py`, aan het einde van `main()`, na de bestaande `generate_index_pages()` aanroep:
```python
    # Genereer leergang-indexpagina's als dit een leergang-les is
    if domein and leergang:
        import subprocess
        result = subprocess.run(
            ['python3', str(script_dir / 'generate-leergangen.py')],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  WAARSCHUWING: leergang-generator fout: {result.stderr}")
        else:
            print(result.stdout)
```

- [ ] **Stap 13.4: Commit**

```bash
git add .github/scripts/generate-leergangen.py
git commit -m "feat: add leergangen index page and search index generator"
```

---

### Taak 14: Homepage bijwerken met twee ingangen

**Bestanden:**
- Wijzigen: `index.html`

- [ ] **Stap 14.1: Voeg twee-ingangen-sectie toe aan homepage**

Zoek in `index.html` de `<div class="container">` en voeg vóór de bestaande auteur-kaarten een sectie toe:

```html
        <!-- Twee ingangen -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:2.5rem;">
            <a href="#schoollessen" style="display:block;background:#2563eb;color:white;border-radius:12px;padding:1.5rem;text-decoration:none;text-align:center;transition:opacity .15s;" onmouseover="this.style.opacity='.85'" onmouseout="this.style.opacity='1'">
                <div style="font-size:2rem;margin-bottom:.5rem;">📚</div>
                <strong style="font-size:1.1rem;">Schoollessen</strong>
                <p style="opacity:.85;font-size:.9rem;margin-top:.25rem;">HAVO, VWO, MBO — per docent</p>
            </a>
            <a href="leergangen/" style="display:block;background:#6366f1;color:white;border-radius:12px;padding:1.5rem;text-decoration:none;text-align:center;transition:opacity .15s;" onmouseover="this.style.opacity='.85'" onmouseout="this.style.opacity='1'">
                <div style="font-size:2rem;margin-bottom:.5rem;">🎓</div>
                <strong style="font-size:1.1rem;">Leergangen</strong>
                <p style="opacity:.85;font-size:.9rem;margin-top:.25rem;">Volwasseneneducatie — per onderwerp</p>
            </a>
        </div>
        <h2 id="schoollessen" style="font-size:1.1rem;color:#64748b;margin-bottom:1rem;font-weight:600;">Schoollessen per docent</h2>
```

- [ ] **Stap 14.2: Commit**

```bash
git add index.html
git commit -m "feat: add two-section homepage (schoollessen + leergangen)"
```

---

### Taak 15: Playwright-tests als kwaliteitsgate in workflow

**Bestanden:**
- Nieuw: `.github/scripts/validate-lesson.spec.js` (hergebruik van C:/temp/playwright-les/les-validatie-v2.spec.js)
- Nieuw: `.github/scripts/playwright.config.js`
- Nieuw: `package.json`
- Wijzigen: `.github/workflows/generate-lesson.yml`

- [ ] **Stap 15.1: Kopieer Playwright-testbestand**

```bash
cp C:/temp/playwright-les/les-validatie-v2.spec.js .github/scripts/validate-lesson.spec.js
```

Pas het bestand aan zodat het lest file via een env-var `LESSON_FILE`:

```javascript
// @ts-check
const { test, expect } = require('@playwright/test');

const LESSON_FILE = process.env.LESSON_FILE;
if (!LESSON_FILE) throw new Error('LESSON_FILE env var vereist');

test.describe('Les validatie', () => {
  test.beforeEach(async ({ page }) => {
    const jsErrors = [];
    page.on('pageerror', err => jsErrors.push(err.message));
    page.on('console', msg => { if (msg.type() === 'error') jsErrors.push(msg.text()); });
    await page.goto('file:///' + LESSON_FILE.replace(/\\/g, '/'));
    page._jsErrors = jsErrors;
  });

  // ... zelfde tests als les-validatie-v2.spec.js maar zonder for-loop
});
```

- [ ] **Stap 15.2: Maak package.json aan**

```json
{
  "name": "claudecodedingetjes",
  "version": "1.0.0",
  "private": true,
  "devDependencies": {
    "@playwright/test": "^1.58.2"
  }
}
```

- [ ] **Stap 15.3: Voeg Playwright-validatiestap toe aan generate-lesson.yml**

Na de `python3 .github/scripts/generate-lesson.py` aanroep, vóór de commit:

```yaml
            # Valideer gegenereerde les met Playwright
            - name: Playwright installeren (eenmalig gecached)
              run: npx playwright install chromium --with-deps

            - name: Les valideren
              env:
                LESSON_FILE: ${{ env.GENERATED_LESSON_PATH }}
              run: |
                npx playwright test .github/scripts/validate-lesson.spec.js \
                  --config=.github/scripts/playwright.config.js
```

> **Opmerking:** `GENERATED_LESSON_PATH` moet als env-var worden gezet na de Python-stap via `echo "GENERATED_LESSON_PATH=..." >> $GITHUB_ENV`.

- [ ] **Stap 15.4: Commit**

```bash
git add .github/scripts/validate-lesson.spec.js .github/scripts/playwright.config.js package.json
git commit -m "feat: add Playwright quality gate to lesson generation workflow"
```

---

## Fase 5 — Integratie en eindtest

### Taak 16: Handmatige test via workflow_dispatch

- [ ] **Stap 16.1: Push alle commits naar main**

```bash
git push origin main
```

- [ ] **Stap 16.2: Test middelbareschool-les zonder foto's**

Ga naar github.com → repository → Issues → New issue → "Middelbare school — nieuwe les"
- Vak: Wiskunde, Niveau: HAVO bovenbouw, Titel: "Statistiek — gemiddelde en mediaan"
- Geen foto's, omschrijving: "Behandel gemiddelde, mediaan en modus. Maak het interactief."
- Label: `nieuwe-les`
- Verwacht: les gegenereerd in `/rwrw01/wiskunde/havo-bovenbouw/statistiek-...`

- [ ] **Stap 16.3: Test volwassen-educatie les**

Maak issue via "Volwasseneneducatie — nieuwe les":
- Domein: Cyber, Leergang: Netwerken en Protocollen
- Titel: "Poorten en protocollen"
- Omschrijving: tekst van issue #41
- Verwacht: les in `/leergangen/cyber/netwerken-en-protocollen/poorten-en-protocollen/`
- Verwacht: leergangen/index.html bijgewerkt

- [ ] **Stap 16.4: Sluit issue #41 opnieuw in**

Issue #41 was het originele "poorten en protocollen" issue. Heropen het en voeg label `nieuwe-les` toe zodat het opnieuw verwerkt wordt met de nieuwe code.

- [ ] **Stap 16.5: Verifieer homepage**

Open `https://rwrw01.github.io/Claudecodedingetjes/` en controleer:
- Twee ingangen zichtbaar (Schoollessen + Leergangen)
- Leergangen-link werkt
- Zoekfunctie in leergangen-sectie werkt

---

## Bekende beperkingen en vervolgstappen

| Item | Status | Toelichting |
|---|---|---|
| Canvas-visualisaties | Niet in scope | Prompts instrueren SVG; canvas vereist domein-specifieke sjablonen per les |
| Pixtral vs Magistral splitsing | Automatisch | generate-lesson.py kiest pixtral alleen als foto's aanwezig zijn + provider=mistral |
| Playwright-cache in CI | Optimalisatie | Kan later met `actions/cache` gecached worden voor snellere runs |
| leergangen.yml validatie | Niet in scope | Voeg later een schema-validatiestap toe bij push naar leergangen.yml |
| MISTRAL_API_KEY rotatie | Direct vereist | Huidige sleutel is gedeeld in chatsessie — onmiddellijk roteren in Mistral console |
| ANTHROPIC_API_KEY rotatie | Direct vereist | Zelfde — roteren in Anthropic console |
