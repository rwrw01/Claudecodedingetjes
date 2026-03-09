# Schaduwagent POC — Fase 0

Lichtgewicht telemetrie-client voor IT-storingen. De eindgebruiker start de client op het werkstation, de servicedeskmedewerker gebruikt Claude Code in VS Code om de telemetrie te analyseren.

## Architectuur

```
WERKSTATION                          SD-WERKPLEK
┌────────────────────┐               ┌──────────────────────┐
│ Schaduwagent Client│  gedeelde     │ VS Code + Claude Code│
│ (tray + console)   │──── map ────►│ leest sessie-map     │
│ - screenshots      │               │ - analyseert logs    │
│ - OS telemetrie    │               │ - bekijkt screenshots│
│ - gebruikersberichten              │ - stelt diagnose     │
└────────────────────┘               └──────────────────────┘
```

## Installatie

```bash
# Vereist: Python 3.12+
cd poc
pip install -e .
```

## Gebruik

### Met GUI (standaard)
```bash
schaduwagent
```

Start de tray-applicatie en het console-venster. De gebruiker kan berichten typen en screenshots worden automatisch gemaakt.

### Headless (zonder GUI)
```bash
schaduwagent --headless
```

### Opties
```
--sessie-dir PATH          Map voor sessie-data (standaard: ~/schaduwagent-sessies)
--screenshot-interval N    Seconden tussen screenshots (standaard: 30)
--os-scan-interval N       Seconden tussen OS-scans (standaard: 10)
--log-path PATH            Extra logbestanden om te monitoren (meerdere keren)
-v, --verbose              Uitgebreide logging
```

### Voorbeeld met extra logs
```bash
schaduwagent --log-path /var/log/syslog --log-path /opt/app/error.log -v
```

## Sessie-output

Na het starten maakt de client een sessie-map aan:

```
~/schaduwagent-sessies/2026-03-09_091500/
├── events.jsonl              # Alle events als JSON Lines
├── screenshots/
│   ├── screen_001.png        # Screenshots
│   └── ...
├── logs/
│   ├── system_info.json      # Systeeminformatie
│   ├── services_status.json  # Draaiende services
│   └── ...
└── user_messages.jsonl       # Berichten van de gebruiker
```

## Voor de servicedeskmedewerker

Open VS Code met Claude Code en de sessie-map in je workspace:

```
> Lees de sessie in ~/schaduwagent-sessies/2026-03-09_091500/ en vertel me
  wat er aan de hand is

> Bekijk de screenshots en logs, wat is de root cause?

> Kun je een fix-script maken voor dit probleem?
```

## Bouwen als .exe (Windows)

```bash
pip install pyinstaller
pyinstaller schaduwagent.spec
# Output: dist/schaduwagent.exe
```

## Technologie

- **Python 3.12** + PyInstaller voor distributie
- **pystray** (MIT) — system tray icoon
- **Pillow** (MIT) — screenshots
- **psutil** (BSD) — OS telemetrie
- **tkinter** (stdlib) — console venster
