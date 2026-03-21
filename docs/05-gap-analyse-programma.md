# Gap-analyse: lessen uit BIT/AcICT versus huidig programma

## Methode

Deze analyse legt de acht terugkerende faalfactoren uit de BIT/AcICT-rapporten (doc 04, §5.3) naast de twaalf onderwerpen in het huidige programma (doc 02, §3.1–3.12). Per faalfactor wordt beoordeeld: is de bijbehorende vaardigheid voldoende gedekt, gedeeltelijk gedekt, of ontbreekt die?

---

## Overzicht: faalfactoren × huidige dekking

| # | Faalfactor uit BIT-rapporten | Gedekt in huidig programma? | Toelichting |
|---|---|---|---|
| 1 | Onvoldoende kennis opdrachtgever | **Gedeeltelijk** | §3.8 (inkoop) raakt eraan, maar opdrachtgeverschap als vaardigheid — het verschil tussen bestellen en specificeren — ontbreekt als eigenstandig onderwerp |
| 2 | Onduidelijke/wisselende requirements | **Niet gedekt** | Nergens in de 12 onderwerpen wordt geleerd hoe je een goede requirement schrijft of beoordeelt |
| 3 | Te optimistische planning / go-no-go | **Niet gedekt** | Geen onderwerp behandelt het beoordelen van haalbaarheid, het herkennen van rode vlaggen in planningen, of het nemen van een stop-besluit |
| 4 | Scope creep / MVP-denken | **Niet gedekt** | Procesdenken (§3.11) raakt aan "eerst proces, dan tool", maar het opdelen van projecten in beheersbare stappen ontbreekt |
| 5 | Ketenblindheid | **Niet gedekt** | Geen onderwerp leert hoe je een ketentekening maakt: welke systemen leveren data, wie is verantwoordelijk, waar zitten de breekpunten |
| 6 | Beleid niet digitaal uitvoerbaar | **Niet gedekt** | De synthese (§6.1) noemt "digitaal vaardig beleid" als hoge prioriteit, maar het onderwerphoofdstuk bevat geen module hierover |
| 7 | Vendor lock-in | **Gedekt** | §3.8 behandelt dit expliciet met GIBIT, dataportabiliteit en open standaarden |
| 8 | Legacy onderschat | **Gedekt** | §3.10 behandelt technische schuld, signalen van einde levensduur en risicoanalyse |

**Score: 2 van 8 volledig gedekt, 1 gedeeltelijk, 5 ontbreken.**

---

## De vijf ontbrekende onderwerpen — uitgewerkt

### Ontbrekend onderwerp A: Opdrachtgeverschap ICT

**Waarom het ontbreekt en waarom het ertoe doet**

De BIT/AcICT-rapporten noemen "onvoldoende kennis bij de opdrachtgever" als de meest voorkomende faalfactor. Bij oBRP lag het probleem niet bij de programmeurs maar bij de organisatie die niet wist wat ze wilde. Bij PGB werd doorgedrukt ondanks rode vlaggen. Bij KEI groeide de scope omdat niemand "nee" zei.

Het huidige programma leert medewerkers over inkoop en contracten (§3.8), maar dat is het einde van het traject. Wat ontbreekt is het begin: de vaardigheid om als opdrachtgever — wethouder, directeur, programmamanager — een ICT-project te sturen zonder zelf technicus te zijn.

**Wat de module moet bevatten**
- Het verschil tussen opdrachtgever en opdrachtnemer helder maken
- Vijf vragen die elke opdrachtgever moet stellen vóór het eerste projectbesluit
- Herkennen wanneer een adviseur of leverancier stuurt in plaats van adviseert
- Casuïstiek: oBRP en PGB als spiegelcasus — "waar had u ingegrepen?"

**Doelgroepen:** Bestuurders (primair), managers (secundair)

**Voorgestelde positie in programma:** Nieuw onderwerp §3.13

---

### Ontbrekend onderwerp B: Requirements management

**Waarom het ontbreekt en waarom het ertoe doet**

Bij oBRP veranderden de eisen voortdurend. Bij DSO waren de eisen zo vaag dat leveranciers ze elk op hun eigen manier interpreteerden. Bij KEI werden eisen tijdens de bouw toegevoegd. De BIT-rapporten noemen dit structureel als faalfactor nummer twee.

Het huidige programma behandelt procesdenken (§3.11) — "beschrijf je werkproces in vijf stappen" — maar maakt de stap niet naar: hoe vertaal je dat proces naar een eis die een leverancier begrijpt en die je kunt toetsen?

**Wat de module moet bevatten**
- Het verschil tussen een wens, een functionele requirement en een technische specificatie
- Drie kenmerken van een goede requirement: specifiek, toetsbaar, prioriteerbaar (MoSCoW)
- Oefening: een bestaand beleidsdocument vertalen naar vijf concrete requirements
- Anti-patronen herkennen: "het systeem moet gebruiksvriendelijk zijn" is geen requirement

**Doelgroepen:** Beleidsmakers (primair), managers (secundair)

**Voorgestelde positie in programma:** Nieuw onderwerp §3.14

---

### Ontbrekend onderwerp C: Go/no-go en projectbeheersing

**Waarom het ontbreekt en waarom het ertoe doet**

Het PGB-systeem werd ingevoerd terwijl intern al bekend was dat het niet klaar was. Bij DSO negeerde het programma het BIT-advies om op te knippen. Bij oBRP duurde het dertien jaar voordat iemand stopte. De AcICT-aanbeveling "organiseer aanpassingsvermogen — plan tegenvallers in" is een directe reactie op dit patroon.

Het huidige programma behandelt risicomanagement (§3.12), maar dat richt zich op bedrijfscontinuïteit (ransomware, uitval). Wat ontbreekt is projectrisico: hoe beoordeel je of een lopend ICT-project op koers ligt, en wanneer stop je?

**Wat de module moet bevatten**
- Wat een go/no-go besluit inhoudt en wie het neemt
- Vijf rode vlaggen in ICT-projecten (scope groeit, mijlpalen schuiven, leverancier vervangt mensen, testresultaten ontbreken, "het komt goed"-communicatie)
- Het sunk cost-probleem: waarom stoppen moeilijker is dan doorgaan
- MVP-denken: hoe je een groot project opknipt in werkende tussenresultaten
- Oefening: een fictieve projectrapportage beoordelen — ga je door of stop je?

**Doelgroepen:** Bestuurders (primair), beleidsmakers (primair), managers (secundair)

**Voorgestelde positie in programma:** Nieuw onderwerp §3.15

---

### Ontbrekend onderwerp D: Ketendenken en ketenregie

**Waarom het ontbreekt en waarom het ertoe doet**

Bij PGB wist de SVB niet welke data gemeenten en zorgkantoren konden aanleveren. Bij DSO werkten tientallen partijen met verschillende systemen die op elkaar moesten aansluiten. De AcICT noemt ketenblindheid — "partijen kennen elkaars beperkingen niet" — als een structureel probleem.

Het huidige programma behandelt geen enkel onderwerp dat expliciet gaat over ketens: wie levert welke data, in welk formaat, op welk moment, en wat gebeurt er als één schakel faalt?

**Wat de module moet bevatten**
- Wat een keten is in de context van overheid en zorg (voorbeeld: aanvraag bijstand raakt UWV, SVB, gemeente, belastingdienst)
- Een eenvoudige ketentekening maken: systemen, datastromen, verantwoordelijkheden
- Drie vragen per ketenpartner: wat lever je, wat heb je nodig, wat kan er misgaan?
- Casuïstiek: PGB als voorbeeld van een keten die niemand overzag
- Het verschil tussen technische koppeling en organisatorische afspraak

**Doelgroepen:** Beleidsmakers (primair), managers (primair), bestuurders (secundair)

**Voorgestelde positie in programma:** Nieuw onderwerp §3.16

---

### Ontbrekend onderwerp E: Digitaal uitvoerbaar beleid

**Waarom het ontbreekt en waarom het ertoe doet**

De eerste aanbeveling van het AcICT luidt: "Pak door op digitaal vaardig beleid — toets uitvoerbaarheid al bij wetgeving." Bij PGB schreef de wetgever regels die data-uitwisseling vereisten die technisch onmogelijk bleek. De toeslagenaffaire was mede het gevolg van wetgeving die werd geautomatiseerd zonder de consequenties te doordenken.

Het huidige programma noemt dit in de synthese (§6.1: "digitaal vaardig beleid maken", prioriteit H voor bestuurders en beleidsmakers), maar bevat geen bijbehorend onderwerp in de twaalf modules.

**Wat de module moet bevatten**
- Wat "uitvoerbaarheid" betekent vóórdat een beleidsvoorstel naar de raad of het bestuur gaat
- De uitvoeringstoets: vier vragen over elk beleidsvoorstel met een digitale component
  1. Welke data is nodig en is die beschikbaar?
  2. Welke systemen moeten worden aangepast en wat kost dat?
  3. Welke ketenpartners zijn betrokken en zijn zij gereed?
  4. Wat zijn de gevolgen als het systeem niet op tijd klaar is?
- De toeslagenaffaire-les: automatisering versterkt fouten in beleid
- Oefening: een bestaand raadsvoorstel of bestuursbesluit toetsen op digitale uitvoerbaarheid

**Doelgroepen:** Beleidsmakers (primair), bestuurders (primair)

**Voorgestelde positie in programma:** Nieuw onderwerp §3.17

---

## Impact op de leergangstructuur

### Huidige kernmodules (doc 04, §6.4)
1. Digitaal Fundament (iedereen, 1 dag)
2. Opdrachtgeverschap (leidinggevenden, 1 dag)
3. Ketendenken (beleidsmakers/projectleiders, halve dag)
4. Digitale Weerbaarheid (iedereen, halve dag)

### Probleem
De kernmodules 2 en 3 (Opdrachtgeverschap en Ketendenken) worden al als kernmodule voorgesteld in de synthese, maar hebben **geen bijbehorend onderwerpshoofdstuk** in doc 02. Dat betekent dat de trainer geen inhoudelijke uitwerking heeft om op te bouwen.

### Aanbeveling: aangepast programma met 17 onderwerpen

| Categorie | Bestaand | Toe te voegen |
|---|---|---|
| **Basis** (iedereen) | §3.1 Zakelijk vs privé-IT | |
| | §3.2 Data en waarde | |
| | §3.3 Informatiebeveiliging | |
| | §3.4 AI en prompt engineering | |
| | §3.5 Digitale communicatie | |
| | §3.6 Privacy en AVG | |
| | §3.7 Digitale toegankelijkheid | |
| **Organisatie & beleid** | §3.8 Inkoop en leveranciers | **§3.13 Opdrachtgeverschap ICT** |
| | §3.9 Cloud en SaaS | **§3.14 Requirements management** |
| | §3.10 Legacy en technische schuld | **§3.15 Go/no-go en projectbeheersing** |
| | §3.11 Procesdenken | **§3.16 Ketendenken en ketenregie** |
| | §3.12 Risicomanagement | **§3.17 Digitaal uitvoerbaar beleid** |

### Prioritering

Als er maar ruimte is voor drie van de vijf nieuwe onderwerpen:

1. **§3.13 Opdrachtgeverschap** — dekt de meest genoemde faalfactor (onvoldoende kennis opdrachtgever) en is relevant voor twee doelgroepen
2. **§3.16 Ketendenken** — dekt de faalfactor die de meeste maatschappelijke schade heeft veroorzaakt (PGB) en is relevant voor drie doelgroepen
3. **§3.15 Go/no-go en projectbeheersing** — dekt het patroon van doormodderen dat honderden miljoenen heeft gekost

---

## Samenvatting

Het huidige programma is sterk op het niveau van individuele digitale vaardigheden (phishing herkennen, AVG toepassen, AI verantwoord gebruiken). Het is zwak op het niveau van **organisatorisch en bestuurlijk digitaal vakmanschap** — precies het niveau waar de BIT/AcICT-rapporten de grootste schade documenteren.

De vijf ontbrekende onderwerpen vullen die lacune. Ze richten zich primair op bestuurders, managers en beleidsmakers — de doelgroepen die beslissingen nemen over projecten van tienduizenden tot honderden miljoenen euro's, zonder de vaardigheden om die beslissingen te onderbouwen.

Zonder deze aanvullingen traint de leergang medewerkers om phishingmails te herkennen, maar niet de bestuurders om te voorkomen dat het volgende oBRP of PGB-debacle zich herhaalt.
