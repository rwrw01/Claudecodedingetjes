"""Genereer visuele screenshots/mockups voor de POC documentatie."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

DOCS = Path(__file__).parent
OUT = DOCS / "screenshots"
OUT.mkdir(exist_ok=True)

# Catppuccin Mocha kleuren
BG = "#1e1e2e"
SURFACE = "#313244"
OVERLAY = "#45475a"
TEXT = "#cdd6f4"
SUBTEXT = "#bac2de"
DIM = "#6c7086"
GREEN = "#a6e3a1"
BLUE = "#89b4fa"
RED = "#f38ba8"
YELLOW = "#f9e2af"
PEACH = "#fab387"
MAUVE = "#cba6f7"


def fig_console_mockup():
    """Screenshot 1: Console-venster mockup."""
    fig, ax = plt.subplots(1, 1, figsize=(7, 6.5), facecolor=BG)
    ax.set_xlim(0, 520)
    ax.set_ylim(0, 480)
    ax.set_aspect("equal")
    ax.axis("off")

    # Window frame
    ax.add_patch(patches.FancyBboxPatch((5, 5), 510, 470, boxstyle="round,pad=8",
                                         facecolor=BG, edgecolor=OVERLAY, linewidth=2))

    # Header bar
    ax.add_patch(patches.FancyBboxPatch((10, 430), 500, 40, boxstyle="round,pad=4",
                                         facecolor=SURFACE, edgecolor="none"))
    ax.text(25, 450, "Schaduwagent", fontsize=13, fontweight="bold", color=TEXT, fontfamily="monospace")
    ax.text(180, 450, "● Sessie actief", fontsize=10, color=GREEN, fontfamily="monospace")
    ax.text(440, 450, "00:03:42", fontsize=10, color=SUBTEXT, fontfamily="monospace")

    # Chat messages
    y = 400
    messages = [
        ("Agent", BLUE, "Sessie gestart. De servicedesk kan nu meekijken."),
        ("Jij", GREEN, "kijk hier gaat t verkeerd als ik op opslaan klik"),
        ("Agent", BLUE, "Begrepen, ik heb een screenshot gemaakt en\nje bericht doorgestuurd."),
        ("Jij", GREEN, "ik krijg steeds een witte pagina"),
        ("Agent", BLUE, "Genoteerd. De servicedesk bekijkt het nu."),
    ]

    for sender, color, text in messages:
        y -= 15
        ax.text(25, y, f"[{sender}]", fontsize=9, color=color, fontweight="bold", fontfamily="monospace")
        lines = text.split("\n")
        for line in lines:
            y -= 15
            ax.text(25, y, line, fontsize=9, color=TEXT if sender == "Agent" else color, fontfamily="monospace")
        y -= 10

    # Input bar
    ax.add_patch(patches.FancyBboxPatch((10, 15), 500, 45, boxstyle="round,pad=4",
                                         facecolor=SURFACE, edgecolor="none"))
    ax.add_patch(patches.FancyBboxPatch((15, 25), 350, 28, boxstyle="round,pad=3",
                                         facecolor=OVERLAY, edgecolor=BLUE, linewidth=1))
    ax.text(25, 38, "Typ je bericht...", fontsize=9, color=DIM, fontfamily="monospace")

    # Send button
    ax.add_patch(patches.FancyBboxPatch((375, 25), 35, 28, boxstyle="round,pad=3",
                                         facecolor=BLUE, edgecolor="none"))
    ax.text(386, 38, ">", fontsize=12, fontweight="bold", color=BG, fontfamily="monospace")

    # Stop button
    ax.add_patch(patches.FancyBboxPatch((420, 25), 85, 28, boxstyle="round,pad=3",
                                         facecolor=RED, edgecolor="none"))
    ax.text(432, 37, "Stop sessie", fontsize=8, color=BG, fontweight="bold", fontfamily="monospace")

    fig.savefig(OUT / "console-venster.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {OUT / 'console-venster.png'}")


def fig_poc_architectuur():
    """Screenshot 2: POC architectuur diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6), facecolor=BG)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 500)
    ax.set_aspect("equal")
    ax.axis("off")

    # Werkstation box
    ax.add_patch(patches.FancyBboxPatch((30, 50), 400, 400, boxstyle="round,pad=10",
                                         facecolor=SURFACE, edgecolor=BLUE, linewidth=2))
    ax.text(130, 420, "WERKSTATION", fontsize=12, fontweight="bold", color=BLUE, fontfamily="monospace")
    ax.text(90, 400, "(eindgebruiker)", fontsize=9, color=DIM, fontfamily="monospace")

    # Client components
    components = [
        (60, 330, 160, 50, "System Tray", GREEN, "Start/stop sessie"),
        (240, 330, 160, 50, "Console", GREEN, "Gebruikersberichten"),
        (60, 250, 160, 50, "Screenshot", PEACH, "Schermopname"),
        (240, 250, 160, 50, "OS Telemetrie", PEACH, "CPU/RAM/services"),
        (60, 170, 160, 50, "Log Collector", PEACH, "Event logs"),
        (240, 170, 160, 50, "Sessie Manager", YELLOW, "JSONL events"),
    ]

    for x, y, w, h, label, color, sub in components:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=4",
                                             facecolor=BG, edgecolor=color, linewidth=1.5))
        ax.text(x + 10, y + 30, label, fontsize=9, fontweight="bold", color=color, fontfamily="monospace")
        ax.text(x + 10, y + 12, sub, fontsize=7, color=DIM, fontfamily="monospace")

    # Sessie-map output
    ax.add_patch(patches.FancyBboxPatch((60, 70), 340, 75, boxstyle="round,pad=6",
                                         facecolor=BG, edgecolor=YELLOW, linewidth=1.5, linestyle="dashed"))
    ax.text(80, 125, "sessies/2026-03-09_001/", fontsize=9, fontweight="bold", color=YELLOW, fontfamily="monospace")
    ax.text(80, 108, "├─ events.jsonl", fontsize=8, color=TEXT, fontfamily="monospace")
    ax.text(80, 93, "├─ screenshots/", fontsize=8, color=TEXT, fontfamily="monospace")
    ax.text(80, 78, "└─ logs/", fontsize=8, color=TEXT, fontfamily="monospace")

    # Arrow: gedeelde map
    ax.annotate("", xy=(570, 250), xytext=(440, 250),
                arrowprops=dict(arrowstyle="->", color=YELLOW, lw=3))
    ax.text(455, 270, "gedeelde\nmap / repo", fontsize=9, color=YELLOW, fontfamily="monospace",
            ha="center", linespacing=1.5)

    # SD Werkplek box
    ax.add_patch(patches.FancyBboxPatch((570, 50), 400, 400, boxstyle="round,pad=10",
                                         facecolor=SURFACE, edgecolor=MAUVE, linewidth=2))
    ax.text(640, 420, "SD-WERKPLEK", fontsize=12, fontweight="bold", color=MAUVE, fontfamily="monospace")
    ax.text(625, 400, "(servicedeskmedewerker)", fontsize=9, color=DIM, fontfamily="monospace")

    # VS Code + Claude Code
    ax.add_patch(patches.FancyBboxPatch((600, 130), 340, 240, boxstyle="round,pad=8",
                                         facecolor=BG, edgecolor=MAUVE, linewidth=1.5))
    ax.text(620, 345, "VS Code + Claude Code", fontsize=11, fontweight="bold", color=MAUVE, fontfamily="monospace")

    # Claude conversation
    claude_lines = [
        (BLUE, '> "Wat zie je in de sessie?"'),
        (TEXT, ""),
        (MAUVE, "Claude: ESB proxy gecrasht door"),
        (MAUVE, "geheugentekort. Service 'esb-proxy'"),
        (MAUVE, "is gestopt."),
        (TEXT, ""),
        (MAUVE, "DIAGNOSE: OutOfMemoryException"),
        (MAUVE, "ACTIE: Herstart service"),
    ]
    y = 310
    for color, text in claude_lines:
        ax.text(620, y, text, fontsize=8, color=color, fontfamily="monospace")
        y -= 18

    # Sessie-map in VS Code
    ax.add_patch(patches.FancyBboxPatch((600, 70), 340, 50, boxstyle="round,pad=4",
                                         facecolor=BG, edgecolor=YELLOW, linewidth=1, linestyle="dashed"))
    ax.text(620, 98, "Leest: events.jsonl + screenshots + logs", fontsize=8, color=YELLOW, fontfamily="monospace")
    ax.text(620, 80, "Geen backend nodig!", fontsize=8, fontweight="bold", color=GREEN, fontfamily="monospace")

    fig.savefig(OUT / "poc-architectuur.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {OUT / 'poc-architectuur.png'}")


def fig_sessie_output():
    """Screenshot 3: Voorbeeld sessie-output (events.jsonl)."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 5), facecolor=BG)
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 400)
    ax.set_aspect("equal")
    ax.axis("off")

    # Title
    ax.text(20, 375, "events.jsonl — Telemetrie stream", fontsize=13, fontweight="bold",
            color=TEXT, fontfamily="monospace")
    ax.add_patch(patches.Rectangle((15, 360), 770, 2, facecolor=OVERLAY))

    events = [
        ('09:01:12', 'session_start', GREEN, '"hostname": "WS-042", "os": "Windows 11 Pro"'),
        ('09:01:12', 'system_info', BLUE, '"cpu_count": 8, "ram_total_gb": 16.0'),
        ('09:01:12', 'screenshot', PEACH, '"file": "screenshots/screen_001.png", "trigger": "session_start"'),
        ('09:01:13', 'os_scan', YELLOW, '"cpu": "12%", "mem": "68%", "services_down": ["esb-proxy"]'),
        ('09:01:15', 'user_message', GREEN, '"text": "kijk hier gaat t verkeerd als ik op opslaan klik"'),
        ('09:01:16', 'screenshot', PEACH, '"file": "screenshots/screen_002.png", "trigger": "user_message"'),
        ('09:01:18', 'log_fragment', RED, '"source": "esb-proxy.log", "lines": ["OutOfMemoryException..."]'),
        ('09:05:00', 'session_stop', DIM, '"elapsed": "00:03:48"'),
    ]

    y = 340
    for ts, etype, color, data in events:
        # Timestamp
        ax.text(20, y, ts, fontsize=8, color=DIM, fontfamily="monospace")
        # Event type badge
        ax.add_patch(patches.FancyBboxPatch((90, y - 6), len(etype) * 7.5 + 10, 18,
                                             boxstyle="round,pad=2", facecolor=color + "33", edgecolor=color, linewidth=1))
        ax.text(97, y, etype, fontsize=8, fontweight="bold", color=color, fontfamily="monospace")
        # Data
        data_x = 105 + len(etype) * 7.5 + 15
        ax.text(data_x, y, data, fontsize=7.5, color=SUBTEXT, fontfamily="monospace")
        y -= 38

    fig.savefig(OUT / "sessie-output.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {OUT / 'sessie-output.png'}")


def fig_tray_mockup():
    """Screenshot 4: System tray mockup."""
    fig, ax = plt.subplots(1, 1, figsize=(5, 4), facecolor=BG)
    ax.set_xlim(0, 350)
    ax.set_ylim(0, 280)
    ax.set_aspect("equal")
    ax.axis("off")

    # Tray menu
    ax.add_patch(patches.FancyBboxPatch((20, 20), 310, 240, boxstyle="round,pad=8",
                                         facecolor=SURFACE, edgecolor=OVERLAY, linewidth=2))

    # Header
    ax.text(50, 235, "●", fontsize=16, color=GREEN, fontfamily="monospace")
    ax.text(75, 235, "Schaduwagent", fontsize=12, fontweight="bold", color=TEXT, fontfamily="monospace")
    ax.text(75, 215, "Sessie actief", fontsize=9, color=GREEN, fontfamily="monospace")
    ax.add_patch(patches.Rectangle((30, 205), 280, 1, facecolor=OVERLAY))

    # Menu items
    items = [
        ("Start sessie", DIM, False),
        ("Stop sessie", RED, True),
        ("Open console", TEXT, True),
        ("─────────────", OVERLAY, False),
        ("Afsluiten", TEXT, True),
    ]

    y = 185
    for label, color, enabled in items:
        if label.startswith("─"):
            ax.add_patch(patches.Rectangle((30, y + 5), 280, 1, facecolor=OVERLAY))
        else:
            if enabled:
                ax.add_patch(patches.FancyBboxPatch((30, y - 4), 280, 25, boxstyle="round,pad=2",
                                                     facecolor=OVERLAY + "44", edgecolor="none"))
            ax.text(45, y + 5, label, fontsize=10, color=color,
                    fontfamily="monospace", alpha=0.4 if not enabled else 1.0)
        y -= 35

    fig.savefig(OUT / "tray-menu.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {OUT / 'tray-menu.png'}")


if __name__ == "__main__":
    print("Screenshots genereren...")
    fig_console_mockup()
    fig_poc_architectuur()
    fig_sessie_output()
    fig_tray_mockup()
    print("Klaar!")
