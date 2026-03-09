"""Hoofdmodule — koppelt sessie, collector, console en tray aan elkaar."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .collector import Collector
from .config import Config
from .session import Session

# GUI-modules zijn optioneel (niet beschikbaar in headless/server omgevingen)
try:
    from .console import Console
    from .tray import TrayIcon
    _GUI_AVAILABLE = True
except ImportError:
    _GUI_AVAILABLE = False

logger = logging.getLogger("schaduwagent")


class SchaduwagentApp:
    """De schaduwagent applicatie die alle componenten verbindt."""

    def __init__(self, config: Config):
        self.config = config
        self.session = Session(config)
        self.collector = Collector(self.session, config)
        self.console = None
        self.tray = None

        if _GUI_AVAILABLE:
            self.console = Console(
                config,
                on_message=self._on_user_message,
                on_stop=self.stop_session,
            )
            self.tray = TrayIcon(
                on_start=self.start_session,
                on_stop=self.stop_session,
                on_console=self._show_console,
                on_quit=self.quit,
            )

    def start_session(self):
        """Start een nieuwe sessie met telemetrie-verzameling."""
        if self.session.active:
            logger.info("Sessie al actief")
            return

        session_dir = self.session.start()
        self.collector.start()
        if self.tray:
            self.tray.set_active(True)

        # Initieel screenshot
        self.collector.take_screenshot(trigger="session_start")

        # Verzamel logs
        self.collector.collect_logs()

        logger.info("Sessie gestart: %s", session_dir)
        if self.console:
            self.console.add_agent_response(
                f"Sessie gestart. Telemetrie wordt geschreven naar:\n{session_dir}"
            )

    def stop_session(self):
        """Stopt de actieve sessie."""
        if not self.session.active:
            return

        self.collector.stop()
        self.session.stop()
        if self.tray:
            self.tray.set_active(False)
        logger.info("Sessie gestopt")

    def quit(self):
        """Sluit de applicatie volledig af."""
        self.stop_session()
        if self.tray:
            self.tray.stop()
        sys.exit(0)

    def _on_user_message(self, text: str):
        """Verwerkt een bericht van de gebruiker via de console."""
        if not self.session.active:
            if self.console:
                self.console.add_agent_response("Er is geen actieve sessie. Start eerst een sessie.")
            return

        # Schrijf het bericht naar de sessie
        self.session.write_user_message(text)

        # Screenshot bij gebruikersbericht
        if self.config.screenshot_on_user_message:
            self.collector.take_screenshot(trigger="user_message")

        # Bevestig aan de gebruiker
        if self.console:
            self.console.add_agent_response(
                "Begrepen, ik heb een screenshot gemaakt en je bericht genoteerd. "
                "De servicedesk kan dit nu bekijken."
            )

    def _show_console(self):
        """Toont het console-venster."""
        if self.console:
            self.console.show_in_thread(get_elapsed=lambda: self.session.elapsed)

    def run(self, headless: bool = False):
        """Start de applicatie.

        Args:
            headless: Als True, start direct een sessie zonder GUI (voor testen).
        """
        if headless:
            self._run_headless()
        else:
            self._run_gui()

    def _run_gui(self):
        """Start met tray-icoon en console."""
        if not _GUI_AVAILABLE:
            logger.error("GUI niet beschikbaar (tkinter ontbreekt). Gebruik --headless.")
            sys.exit(1)

        # Start tray in achtergrond
        self.tray.run_in_thread()

        # Start automatisch een sessie
        self.start_session()

        # Console blokkeert de main thread (tkinter vereist main thread)
        self.console.show(get_elapsed=lambda: self.session.elapsed)

    def _run_headless(self):
        """Start zonder GUI — schrijft alleen telemetrie naar sessie-map."""
        self.start_session()
        logger.info("Headless modus. Ctrl+C om te stoppen.")
        try:
            import time
            while self.session.active:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Ctrl+C ontvangen, sessie wordt gestopt...")
            self.stop_session()


def main():
    """Entry point voor de schaduwagent CLI."""
    parser = argparse.ArgumentParser(
        description="Schaduwagent — Lichtgewicht telemetrie-client voor IT-storingen",
    )
    parser.add_argument(
        "--sessie-dir",
        type=Path,
        default=None,
        help="Map voor sessie-data (standaard: ~/schaduwagent-sessies)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Start zonder GUI, alleen telemetrie-verzameling",
    )
    parser.add_argument(
        "--screenshot-interval",
        type=int,
        default=30,
        help="Interval in seconden tussen screenshots (standaard: 30)",
    )
    parser.add_argument(
        "--os-scan-interval",
        type=int,
        default=10,
        help="Interval in seconden tussen OS-scans (standaard: 10)",
    )
    parser.add_argument(
        "--log-path",
        action="append",
        default=[],
        help="Extra logbestanden om te monitoren (kan meerdere keren)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Uitgebreide logging",
    )

    args = parser.parse_args()

    # Logging configuratie
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Configuratie opbouwen
    config = Config(
        screenshot_interval_sec=args.screenshot_interval,
        os_scan_interval_sec=args.os_scan_interval,
        log_paths=args.log_path,
    )
    if args.sessie_dir:
        config.sessie_root = args.sessie_dir

    # Start de applicatie
    app = SchaduwagentApp(config)
    app.run(headless=args.headless)


if __name__ == "__main__":
    main()
