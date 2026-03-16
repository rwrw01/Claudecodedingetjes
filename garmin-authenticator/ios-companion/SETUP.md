# iOS Companion App - Setup Instructies

## Vereisten
- Xcode 15+
- iOS 16+ apparaat
- Garmin Connect IQ Mobile SDK

## Stap 1: Garmin Connect IQ Mobile SDK toevoegen

1. Download de SDK van: https://developer.garmin.com/connect-iq/sdk/
2. Pak `ConnectIQ.framework` uit
3. Sleep het framework naar het Xcode project
4. Ga naar Target → General → Frameworks → voeg `ConnectIQ.framework` toe

## Stap 2: URL Scheme instellen

1. Ga naar Target → Info → URL Types
2. Voeg toe: `garminauth` (dit is nodig voor de Connect IQ terugkoppeling)

## Stap 3: Project openen

```bash
cd ios-companion/GarminAuth
open GarminAuth.xcodeproj
```

## Stap 4: Build & Run

1. Selecteer je iPhone als doel
2. Cmd+R om te bouwen en te draaien
3. De app vraagt om notificatie-toestemming

## Stap 5: Garmin horloge koppelen

1. Zorg dat je horloge via Bluetooth verbonden is met je iPhone
2. Open de Garmin Auth app
3. De app zoekt automatisch naar je horloge

## Gebruik

1. Log in bij een Microsoft-dienst op je PC
2. Microsoft toont een 2-cijferig nummer
3. Open Garmin Auth op je iPhone
4. Voer het nummer in
5. Het nummer verschijnt op je Garmin horloge
6. Kies het juiste nummer op je horloge → inloggen bevestigd!

## Productie-uitrol

Om de `GarminManager` te laten werken met een echt horloge:
1. Verwijder de simulatie-code in `GarminManager.swift`
2. Uncomment de `ConnectIQ.framework` aanroepen
3. Vervang de app UUID met je eigen Connect IQ app ID
