# Lessen uit het College ICT-toetsing en synthese

## 5. Lessen uit het College ICT-toetsing (BIT/AcICT)

### 5.1 Achtergrond

Na jaren van mislukte overheids-ICT-projecten stelde de Tweede Kamer in 2012 de Tijdelijke Commissie ICT in onder leiding van Ton Elias. De commissie concludeerde dat jaarlijks 1 tot 5 miljard euro belastinggeld verloren gaat door falende digitale projecten, en dat een op de vijf grote ICT-projecten nooit van de grond komt. Op haar advies werd in 2015 het **Bureau ICT-toetsing (BIT)** opgericht, dat eind 2020 overging in het **Adviescollege ICT-toetsing (AcICT)**.

De vijf terugkerende aanbevelingen van het AcICT (2023):
1. Pak door op **digitaal vaardig beleid** — toets uitvoerbaarheid al bij wetgeving
2. Werk aan **kennis van ICT-beheersing** bij management en opdrachtgevers
3. Verhelp **legacy evolutionair** — kleine stappen, geen reuzesprongen
4. **Maak concreet** welk probleem het project moet oplossen
5. **Organiseer aanpassingsvermogen** — plan tegenvallers in

### 5.2 Bekende projecten die zijn mislukt

#### Operatie BRP — stopgezet 2017, >€100 miljoen
Na 13 jaar en ruim 100 miljoen euro stopgezet. Een "eenvoudig" idee: moderne database van persoonsgegevens. De softwaregeneratoren werkten nooit, code was handmatig herschreven. Maar de eigenlijke problemen lagen bij de **opdrachtgever**: wisselende eisen, geen stabiel ontwerp, versnipperde organisatie. Gemeenten waren 54 miljoen kwijt aan aansluitkosten voor een systeem dat er nooit kwam.

**Les:** Als de gemeentesecretaris had geweten dat requirements management de meest kritische vaardigheid is — niet technische kennis — was eerder ingegrepen.

#### PGB Trekkingsrecht (SVB) — 2015, €156 miljoen
Per 1 januari 2015 moest de SVB het PGB administreren via een nieuw systeem. In oktober 2014 was intern al bekend dat het niet klaar was. Toch ging de invoering door. Resultaat: dagelijks 80 nieuwe meldingen over betalingsachterstanden, zorgverleners die weken op salaris wachtten.

**Les:** Als een beleidsmedewerker had geweten hoe een ketenanalyse te lezen — wie levert welke data, wanneer, in welk formaat — was direct duidelijk geweest dat het systeem niet kon functioneren.

#### Digitaal Stelsel Omgevingswet (DSO) — lopend, €200 miljoen+
In 2017 waarschuwde het BIT dat het te complex was. In 2024: gemiddeld 2,5 storingen per dag, twee op drie gemeenten vallen terug op tijdelijke alternatieven. Een ICT-adviseur: "Er zijn veel managers actief en te weinig ambachtslieden die het geheel overzien."

**Les:** Als de informatiearchitect had geweten hoe je afhankelijkheden en faalrisico's beoordeelt, was de beslissing om in de TAM-variant te blijven eerder en bewuster genomen.

#### KEI (rechtspraak) — stopgezet 2019, >€200 miljoen
Na zes jaar de stekker eruit. Uitvoerbaarheid onvoldoende doordacht, scope voortdurend uitgebreid.

### 5.3 Oorzaken gekoppeld aan vaardigheidstekorten

| Oorzaak uit BIT-rapporten | Voorbeeld | Ontbrekende vaardigheid | Relevante doelgroep |
|---|---|---|---|
| Onvoldoende kennis opdrachtgever | oBRP: kwaliteit code niet beoordeeld | Kritische vragen stellen, IT-voorstel lezen | Bestuurders, managers |
| Onduidelijke/wisselende requirements | oBRP, DSO: eisen bleven veranderen | Functionele requirements schrijven | Beleidsmakers |
| Te optimistische planning | PGB: ingevoerd terwijl niet klaar | Go/no-go op feiten beoordelen | Bestuurders |
| Vendor lock-in | 91% gemeenten bij Microsoft | Contractlezen, exit-strategie eisen | Bestuurders, beleidsmakers |
| Scope creep | DSO: BIT-advies om op te knippen genegeerd | MVP-denken, projectbeheersing | Beleidsmakers, managers |
| Ketenblindheid | PGB: partijen kenden elkaars beperkingen niet | Ketentekening maken | Beleidsmakers, managers |
| Legacy onderschat | DSO, BRP: oude systemen afgeschreven zonder plan | Technische schuld herkennen | Managers, beleidsmakers |
| Beleid niet digitaal uitvoerbaar | PGB: wetgeving vereiste onmogelijke data-uitwisseling | Uitvoeringstoets op beleid | Beleidsmakers |

### 5.4 De grote gemene deler

Het AcICT formuleert het kernprobleem: de overheid vliegt ICT-projecten te groot en te complex aan. "Alle problemen moeten in één keer worden opgelost." Niemand heeft het complete overzicht.

**Conclusie: digitaal vakmanschap is geen luxe, het is de noodzakelijke tegenkracht tegen structureel falen.**

---

## 6. Synthese: van onderzoek naar leergang

### 6.1 Onderwerp × doelgroep (prioriteit)

| Onderwerp | Bestuurders | Managers | Beleidsmakers | Medewerkers |
|---|---|---|---|---|
| IV vs IT basiskennis | H | H | H | H |
| Requirements management | M | M | H | L |
| Inkoop & contractmanagement | H | M | H | L |
| Vendor lock-in & open standaarden | H | M | H | L |
| Risicobeoordeling projecten | H | M | H | L |
| Ketendenken | H | H | H | M |
| AVG & informatiebeveiliging | M | H | H | H |
| Legacy & technische schuld | L | M | H | L |
| Digitaal vaardig beleid maken | H | M | H | L |
| AI & prompt engineering | M | M | M | H |
| Digitale dienstverlening | H | H | M | H |
| Datagedreven werken | M | H | H | M |
| **Opdrachtgeverschap ICT** | **H** | **M** | **M** | **L** |
| **Ketendenken & ketenregie** | **M** | **H** | **H** | **L** |
| **Digitaal uitvoerbaar beleid** | **H** | **L** | **H** | **L** |

### 6.2 Top 5 quick wins

1. **Checklist voor bestuurders** — vijf vragen voordat een ICT-project groen licht krijgt (gebaseerd op AcICT-criteria)
2. **Contractlezen voor niet-juristen** — halve dag: wat staat er over vendor lock-in, dataportabiliteit, exit?
3. **Ketentekening maken** — één middag per implementatie: welke systemen leveren data, wie is verantwoordelijk, wat kan misgaan?
4. **Informatiefunctionaris aanwijzen** — één persoon verantwoordelijk voor datakwaliteit (niet per se ICT'er)
5. **Eindgebruiker betrekken vóór aanbesteding** — ochtend gebruikersinterviews levert meer op dan maanden specificeren

### 6.3 Top 5 grootste risico's bij NIET investeren

1. **Miljoenen verdampen** — BRP (€100M), PGB (€156M), KEI (€200M), DSO (€200M+): structureel gevolg van opdrachtgevers die de vragen niet kunnen stellen
2. **Kwetsbare burgers worden de dupe** — PGB-debacle: zorgverleners weken zonder salaris, kwetsbare mensen moesten zelf chaos oplossen
3. **Vendor lock-in vreet aan beleidsvrijheid** — gemeenten die van één leverancier afhankelijk zijn, kunnen geen andere beleidskeuze maken
4. **Cyberincidenten met maatschappelijke ontwrichting** — zonder basiskennis bij leidinggevenden worden verkeerde beslissingen genomen over back-ups en incidentrespons
5. **Te vroeg of te laat stoppen** — zonder vakmanschap paniek bij eerste tegenvallers óf doormodderen vanwege sunk costs

### 6.4 Aanbeveling opbouw leergang

**Principe: modulair, ADKAR-gestuurd, praktijkgericht**

| ADKAR-fase | Betekenis voor leergang | Werkvorm |
|---|---|---|
| Awareness | Herkennen in eigen organisatie | Casuïstiek uit BIT-rapporten, spiegelgesprek |
| Desire | Verbinding met eigen verantwoordelijkheid | Persoonlijk leercontract, rollenspel |
| Knowledge | Concrete kennis | Interactieve modules, werkbladen |
| Ability | Oefenen in veilige context | Simulaties, peer review |
| Reinforcement | Verankeren | Intervisie na 3 en 6 maanden, leernetwerk |

**Kernmodules:**
1. **Digitaal Fundament** (iedereen, 1 dag) — basisbegrippen, BIT-lessen, eigen organisatie in kaart
2. **Opdrachtgeverschap** (leidinggevenden, 1 dag) — de vijf opdrachtgeversvragen, rode vlaggen herkennen, go/no-go (onderbouwd door §3.13)
3. **Ketendenken** (beleidsmakers/projectleiders, halve dag) — ketentekening in vier stappen, breekpunten identificeren, ketenpartners bevragen (onderbouwd door §3.14)
4. **Digitale Weerbaarheid** (iedereen, halve dag) — informatiebeveiliging, AVG in de praktijk, incidentrespons
5. **Digitaal Uitvoerbaar Beleid** (beleidsmakers/bestuurders, halve dag) — uitvoeringstoets in vier vragen, terugvalscenario's, toeslagenaffaire-reflectie (onderbouwd door §3.15)

**Verdiepingsmodules (keuze):**
- Inkoop en aanbesteding ICT
- Datagedreven werken
- Architectuur en legacy
- Digitale dienstverlening burgerperspectief
- Zorg-specifiek: EPD, vendor lock-in langdurige zorg

Elke module werkt met **echte casuïstiek**. Deelnemers brengen een eigen dossier mee en werken dat uit. De leergang levert geen certificaat van kennis maar een **portfolio van toegepaste vaardigheden**.

---

**Bronnen:**
- [AcICT vijf aanbevelingen — iBestuur](https://ibestuur.nl/artikel/vijf-aanbevelingen-van-het-adviescollege-ict-toetsing/)
- [Lessen Operatie BRP — AG Connect](https://www.agconnect.nl/artikel/lessen-van-operatie-brp)
- [PGB-chaos — NOS Nieuwsuur](https://nos.nl/nieuwsuur/artikel/2026655-pgb-chaos-hardnekkig)
- [DSO dreigt in te storten — Gemeente.nu](https://www.gemeente.nu/ruimte-milieu/omgevingswet/digitaal-stelsel-omgevingswet-dreigt-in-te-storten/)
- [ACM tegen vendor lock-in zorg-ICT — Computable](https://www.computable.nl/artikel/nieuws/overheid/7202907/250449/acm-in-actie-tegen-vendor-lock-in-bij-zorg-ict.html)
- [Gemeenten bezorgd Microsoft-afhankelijkheid — AG Connect](https://www.agconnect.nl/business/datamanagement/gemeenten-steeds-meer-bezorgd-over-afhankelijkheid-microsoft)
- [Parlementair onderzoek ICT — Wikipedia](https://nl.wikipedia.org/wiki/Parlementair_onderzoek_ICT-projecten_bij_de_overheid)
- [Adviescollege ICT-toetsing](https://www.adviescollegeicttoetsing.nl/)
