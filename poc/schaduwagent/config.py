"""Configuratie voor de Schaduwagent client."""

from dataclasses import dataclass, field
from pathlib import Path
import platform


@dataclass
class Config:
    """Configuratie-instellingen voor een schaduwagent-sessie."""

    # Waar sessie-data naartoe geschreven wordt
    sessie_root: Path = field(default_factory=lambda: Path.home() / "schaduwagent-sessies")

    # Screenshot instellingen
    screenshot_interval_sec: int = 30  # Periodieke screenshot elke N seconden
    screenshot_on_user_message: bool = True  # Screenshot bij elk gebruikersbericht
    screenshot_quality: int = 85  # JPEG kwaliteit (0-100)

    # OS telemetrie instellingen
    os_scan_interval_sec: int = 10  # OS scan elke N seconden
    collect_event_log: bool = platform.system() == "Windows"
    collect_services: bool = True
    collect_system_info: bool = True

    # Log collectie
    log_paths: list[str] = field(default_factory=list)  # Extra log bestanden om te monitoren
    log_tail_lines: int = 50  # Laatste N regels per logbestand

    # Console
    console_title: str = "Schaduwagent"
    console_width: int = 520
    console_height: int = 480
