# Plan: Grondslagen van Getallen (Spivak Calculus H1)

## Context
Een nieuwe "geavanceerd" sectie, gericht op volwassenen educatie als voorbereiding op calculus. Gebaseerd op Spivak's Calculus, Hoofdstuk 1: "Basic Properties of Numbers". Dit is GEEN HAVO-materiaal maar een apart niveau.

Het doel: de 12 fundamentele eigenschappen van getallen (P1-P12) interactief uitleggen, zodat volwassen leerlingen de axiomatische basis van de wiskunde begrijpen. Van "dit weet je al uit intuïtie" naar "nu snap je WAAROM het werkt".

## Taalgebruik: B2-niveau Nederlands
**Cruciale aanpak:** We behouden de officiële wiskundige termen (associativiteit, commutativiteit, axioma, identiteitselement, inverse, trichotomie, etc.) maar leggen ze ALTIJD direct uit in gewone taal. Patroon:

- **Eerst de term noemen**, dan meteen in gewone woorden uitleggen
- Voorbeeld: "**Associativiteit** — dat is een moeilijk woord voor iets simpels: het maakt niet uit waar je de haakjes zet."
- Voorbeeld: "**Axioma** — een spelregel die we als waarheid aannemen, zonder bewijs."
- Voorbeeld: "**Identiteitselement** — het 'niets-doen-getal': het getal dat niets verandert als je ermee rekent."
- Voorbeeld: "**Inverse** — het 'tegenovergestelde': het getal dat alles ongedaan maakt."
- Voorbeeld: "**Trichotomie** — drie mogelijkheden, en precies één is waar."

Bij elk nieuw begrip een korte, alledaagse vergelijking of voorbeeld geven. Geen academisch taalgebruik in de uitleg zelf — alleen in de officiële naam van het concept.

## Structuur van de pagina

### A. Inleiding — Waarom dit ertoe doet
- Je kunt rekenen, maar kun je bewijzen WAAROM 2+3 = 3+2?
- Spivak's aanpak: alles opbouwen vanuit 12 spelregels (axioma's)
- Link terug naar de basis-hoofdstukken: "die intuïtie formaliseren we nu"

### B. De rekenregels (P1–P9)

**P1: Associativiteit van optelling** — a + (b + c) = (a + b) + c
- "Het maakt niet uit waar je de haakjes zet bij optellen"
- Interactief: slider met 3 getallen, laat zien dat volgorde van haakjes niet uitmaakt
- Probeer zelf: vul in met concrete getallen

**P2: Identiteitselement optelling** — a + 0 = 0 + a = a
- "Het niets-doen-getal voor optelling: nul. Tel je 0 ergens bij op, dan verandert er niets."
- Probeer zelf: "Welk getal verandert niets bij optelling?"

**P3: Inverse van optelling** — voor elke a bestaat −a zodat a + (−a) = 0
- "Het tegenovergestelde: elk getal heeft een 'tegenhanger' waarmee je weer op 0 uitkomt."
- Definitie van aftrekken: a − b = a + (−b) — "aftrekken IS optellen van het tegenovergestelde"
- Probeer zelf: invullen van de inverse

**P4: Commutativiteit van optelling** — a + b = b + a
- "De volgorde maakt niet uit bij optellen"
- Interactief: twee invoervelden, laat zien dat omdraaien hetzelfde geeft
- Probeer zelf

**P5: Associativiteit van vermenigvuldiging** — a · (b · c) = (a · b) · c
- Zelfde verhaal als P1, maar dan voor vermenigvuldigen

**P6: Identiteitselement vermenigvuldiging** — a · 1 = 1 · a = a
- "Het niets-doen-getal voor vermenigvuldiging: één."
- Benoem dat 1 ≠ 0 (belangrijk!)

**P7: Inverse van vermenigvuldiging** — voor a ≠ 0 bestaat a⁻¹ zodat a · a⁻¹ = 1
- "Elk getal (behalve 0) heeft een 'omgekeerde' waarmee je weer op 1 uitkomt."
- Definitie van deling: a/b = a · b⁻¹
- Waarom niet delen door 0? → Omdat 0 geen inverse heeft
- Probeer zelf: "Wat is de inverse van 5?"

**P8: Commutativiteit van vermenigvuldiging** — a · b = b · a
- "De volgorde maakt niet uit bij vermenigvuldigen"

**P9: Distributiviteit** — a · (b + c) = a · b + a · c
- "De brug tussen optellen en vermenigvuldigen: je mag vermenigvuldiging 'uitdelen' over een som."
- Interactief voorbeeld: laat stap-voor-stap zien hoe je (x+2)(x+3) uitwerkt
- Probeer zelf: pas distributiviteit toe op concrete getallen
- **Eerste bewijzen:** gebruik P1-P9 om te bewijzen:
  - a · 0 = 0 (want a · 0 = a · (0 + 0) = a · 0 + a · 0)
  - (−a) · b = −(a · b)
  - (−a)(−b) = a · b → interactief stap-voor-stap bewijs met invulvelden per stap

### C. De orde-eigenschappen (P10–P12)

**P10: Trichotomie** — voor elk paar a, b geldt precies één van: a = b, a < b, a > b
- "Drie mogelijkheden, en precies één is waar — net als bij een wedstrijd: je wint, verliest, of speelt gelijk."
- Gedefinieerd via verzameling P van positieve getallen
- Interactief: getallenlijngrafiek

**P11: Gesloten onder optelling** — als a > 0 en b > 0, dan a + b > 0
- "Positief plus positief is altijd positief"

**P12: Gesloten onder vermenigvuldiging** — als a > 0 en b > 0, dan a · b > 0
- "Positief keer positief is altijd positief"
- Hieruit volgt: 1 > 0 (want 1 = 1 · 1 en 1 ≠ 0)
- En: als a ≠ 0, dan a² > 0

**Afleidingen met P10-P12:**
- Als a < b, dan a + c < b + c (bewijs met invulstappen)
- Als a < b en c > 0, dan ac < bc
- Als a < b en c < 0, dan ac > bc ("de ongelijkheid draait om!")
- Interactief: slider die laat zien hoe vermenigvuldigen met een negatief getal de ongelijkheid omdraait

### D. Absolute waarde en driehoeksongelijkheid

**Definitie:** |a| = a als a ≥ 0, |a| = −a als a < 0
- "De afstand van een getal tot nul — altijd positief of nul."
- Interactief: getallenlijngrafiek met slider, |a| = afstand tot 0
- Probeer zelf: |−3| = ?, |5| = ?, |0| = ?

**Stelling 1: Driehoeksongelijkheid** — |a + b| ≤ |a| + |b|
- "De 'kortste weg'-regel: de directe afstand is nooit langer dan de omweg."
- Bewijs stap-voor-stap met invulvelden
- Twee methodes: gevallenanalyse EN de slimme truc |a| = √(a²)
- Wanneer geldt gelijkheid? (zelfde teken)
- Wanneer strikte ongelijkheid? (tegengestelde tekens)

### E. Oefenopgaven (12 opgaven, gebaseerd op Spivak Problems 1–8)

Selectie (aangepaste getallen/letters per CLAUDE.md):

1. **Bewijs:** als bx = b voor een b ≠ 0, dan x = 1
2. **Bewijs:** p² − q² = (p − q)(p + q)
3. **Fout zoeken:** de "2 = 1"-drogrede (delen door 0)
4. **Bewijs:** a/b = ac/(bc) als b,c ≠ 0
5. **Bewijs:** a/b + c/d = (ad + bc)/(bd) — link naar kruislings-methode!
6. **Ongelijkheden:** vind alle x waarvoor 3 − x < 5 − 2x
7. **Ongelijkheden:** vind alle x waarvoor 7 − x² < 3
8. **Bewijs:** als a < b, dan −b < −a
9. **Bewijs:** als 0 < a < 1, dan a² < a
10. **Absolute waarde:** schrijf |√3 + √5 − √2 − √7| zonder absolute-waardetekens
11. **Vind alle x:** |x − 4| < 3
12. **Bewijs:** |a + b| = |a| + |b| als a en b hetzelfde teken hebben

## Interactiviteitsaanpak (per CLAUDE.md-regels)
- **Sliders** bij P1, P5 (associativiteit visueel maken), P10-P12 (getallenlijn)
- **Invulvelden per tussenstap** bij alle bewijzen (niet alleen eindantwoord)
- **Stap-voor-stap onthulling** bij langere bewijzen (klik "volgende stap")
- **Probeer-zelf blokken** bij elke eigenschap (minstens 12 stuks in theorie)
- **Getallenlijngrafiek** (canvas) voor absolute waarde en orde

## Wijzigingen aan hub-pagina
**`wiskunde/index.html`:** Nieuwe sectie "Geavanceerd — Calculus-voorbereiding" toevoegen:

```
Onderbouw (klas 1-2)
├── 1. Rekenen — wat doe je eigenlijk?
├── 2. Van getallen naar breuken

HAVO 3
├── 1. Breuken met letters herleiden

HAVO 4
├── 1. Wortelfuncties
├── 2. Machten met gebroken exponenten (binnenkort)
├── 3. Wortelvergelijkingen (binnenkort)

Geavanceerd — Calculus-voorbereiding          ← NIEUW
├── 1. Grondslagen van getallen (P1–P12)
├── 2. (meer hoofdstukken later)
```

## Bestanden
- **Nieuw:** `wiskunde/grondslagen-getallen/index.html`
- **Wijzig:** `wiskunde/index.html` (nieuwe sectie toevoegen)

## Technische aanpak
- Zelfde standalone HTML/CSS/JS patroon als bestaande hoofdstukken
- Zelfde CSS variabelen, `.frac`, `.formula`, `.tip-box`, `.warning-box`, `.example-box`
- Zelfde `checkAnswer()` en `checkTry()` validatiepatronen
- Canvas-element voor getallenlijngrafiek (vergelijkbaar met wortelfuncties)
- Stap-voor-stap bewijzen: tabben of "volgende stap"-knoppen met invulvelden per stap
- Colofon-footer met Ralph Wagter, Claude Code, EUPL-1.2

## Verificatie
- Alle interactieve elementen (sliders, invulvelden, stap-bewijzen) werken
- Alle 12 oefenopgaven controleren: correct/fout/hints/uitwerkingen
- Hub-pagina links kloppen
- Breadcrumb terug naar hub
- Canvas-getallenlijngrafiek rendert correct
