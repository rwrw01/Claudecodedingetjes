"""Telemetrie-collector — verzamelt screenshots, OS-info, services en logs."""

from __future__ import annotations

import json
import logging
import platform
import subprocess
from pathlib import Path
from threading import Event, Thread

import psutil
from PIL import ImageGrab

from .config import Config
from .session import Session

logger = logging.getLogger(__name__)


class Collector:
    """Verzamelt telemetrie en schrijft naar de sessie-map."""

    def __init__(self, session: Session, config: Config):
        self.session = session
        self.config = config
        self._stop_event = Event()
        self._threads: list[Thread] = []

    def start(self):
        """Start de telemetrie-verzameling in achtergrondthreads."""
        self._stop_event.clear()

        # OS scan thread
        t_os = Thread(target=self._os_scan_loop, daemon=True, name="os-scan")
        t_os.start()
        self._threads.append(t_os)

        # Screenshot thread
        t_screen = Thread(target=self._screenshot_loop, daemon=True, name="screenshot")
        t_screen.start()
        self._threads.append(t_screen)

        # Initiële systeeminfo verzamelen
        self._collect_system_info()

        logger.info("Collector gestart")

    def stop(self):
        """Stopt alle verzamelthreads."""
        self._stop_event.set()
        for t in self._threads:
            t.join(timeout=5)
        self._threads.clear()
        logger.info("Collector gestopt")

    def take_screenshot(self, trigger: str = "manual") -> Path | None:
        """Maakt een screenshot en slaat het op in de sessie-map."""
        if not self.session.active:
            return None
        try:
            screenshot_path = self.session.next_screenshot_path(trigger)
            img = ImageGrab.grab()
            img.save(screenshot_path, "PNG", optimize=True)

            self.session.write_event("screenshot", {
                "file": f"screenshots/{screenshot_path.name}",
                "trigger": trigger,
                "resolution": f"{img.width}x{img.height}",
            })
            logger.info("Screenshot: %s (trigger: %s)", screenshot_path.name, trigger)
            return screenshot_path
        except Exception as e:
            logger.warning("Screenshot mislukt: %s", e)
            self.session.write_event("error", {"component": "screenshot", "message": str(e)})
            return None

    def _screenshot_loop(self):
        """Periodieke screenshots."""
        while not self._stop_event.wait(self.config.screenshot_interval_sec):
            if self.session.active:
                self.take_screenshot(trigger="periodic")

    def _os_scan_loop(self):
        """Periodieke OS-scan."""
        while not self._stop_event.wait(self.config.os_scan_interval_sec):
            if self.session.active:
                self._collect_os_scan()

    def _collect_system_info(self):
        """Verzamelt eenmalige systeeminformatie."""
        if not self.config.collect_system_info:
            return

        info = {
            "hostname": platform.node(),
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 1),
        }

        # Schrijf als apart bestand voor makkelijk lezen
        self.session.write_log_file("system_info.json", json.dumps(info, indent=2))
        self.session.write_event("system_info", info)

    def _collect_os_scan(self):
        """Verzamelt periodieke OS-telemetrie: CPU, geheugen, disk, services."""
        try:
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/") if platform.system() != "Windows" else psutil.disk_usage("C:\\")

            scan_data = {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "mem_percent": mem.percent,
                "mem_available_gb": round(mem.available / (1024**3), 1),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 1),
            }

            # Services die down zijn
            if self.config.collect_services:
                down_services = self._check_services()
                if down_services:
                    scan_data["services_down"] = down_services

            self.session.write_event("os_scan", scan_data)

            # Services status als apart bestand (overschrijft elke scan)
            services = self._get_all_services()
            self.session.write_log_file(
                "services_status.json",
                json.dumps(services, indent=2, ensure_ascii=False),
            )

        except Exception as e:
            logger.warning("OS scan mislukt: %s", e)
            self.session.write_event("error", {"component": "os_scan", "message": str(e)})

    def _check_services(self) -> list[str]:
        """Controleer of er services gestopt/gecrasht zijn."""
        down = []
        if platform.system() == "Windows":
            # Op Windows: check services die 'stopped' zijn maar 'auto' start hebben
            try:
                for service in psutil.win_service_iter():
                    info = service.as_dict()
                    if info.get("start_type") == "automatic" and info.get("status") == "stopped":
                        down.append(info.get("name", "unknown"))
            except Exception:
                pass
        else:
            # Op Linux: check systemd failed units
            try:
                result = subprocess.run(
                    ["systemctl", "--failed", "--no-legend", "--plain", "-q"],
                    capture_output=True, text=True, timeout=5,
                )
                for line in result.stdout.strip().split("\n"):
                    if line.strip():
                        parts = line.split()
                        if parts:
                            down.append(parts[0])
            except Exception:
                pass
        return down

    def _get_all_services(self) -> list[dict]:
        """Haalt een lijst op van alle services met status."""
        services = []
        if platform.system() == "Windows":
            try:
                for service in psutil.win_service_iter():
                    info = service.as_dict()
                    services.append({
                        "name": info.get("name"),
                        "display_name": info.get("display_name"),
                        "status": info.get("status"),
                        "start_type": info.get("start_type"),
                    })
            except Exception:
                pass
        else:
            # Linux: gebruik systemctl
            try:
                result = subprocess.run(
                    ["systemctl", "list-units", "--type=service", "--no-legend", "--plain"],
                    capture_output=True, text=True, timeout=5,
                )
                for line in result.stdout.strip().split("\n"):
                    parts = line.split(None, 4)
                    if len(parts) >= 4:
                        services.append({
                            "name": parts[0],
                            "load": parts[1],
                            "active": parts[2],
                            "sub": parts[3],
                            "description": parts[4] if len(parts) > 4 else "",
                        })
            except Exception:
                pass
        return services

    def collect_logs(self):
        """Verzamelt logbestanden geconfigureerd in config.log_paths."""
        for log_path_str in self.config.log_paths:
            log_path = Path(log_path_str)
            if not log_path.exists():
                continue
            try:
                # Lees laatste N regels
                lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
                tail = lines[-self.config.log_tail_lines:]
                content = "\n".join(tail)

                safe_name = log_path.name.replace("/", "_").replace("\\", "_")
                self.session.write_log_file(safe_name, content)
                self.session.write_event("log_fragment", {
                    "source": str(log_path),
                    "lines_count": len(tail),
                })
            except Exception as e:
                logger.warning("Log collectie mislukt voor %s: %s", log_path, e)

        # Windows Event Log (als geconfigureerd)
        if self.config.collect_event_log and platform.system() == "Windows":
            self._collect_windows_event_log()

    def _collect_windows_event_log(self):
        """Verzamelt recente Windows Event Log entries."""
        try:
            result = subprocess.run(
                ["powershell", "-Command",
                 "Get-EventLog -LogName System -Newest 50 -EntryType Error,Warning | "
                 "Select-Object TimeGenerated,EntryType,Source,Message | "
                 "ConvertTo-Json"],
                capture_output=True, text=True, timeout=15,
            )
            if result.stdout.strip():
                self.session.write_log_file("eventlog_system.json", result.stdout)
                self.session.write_event("log_fragment", {
                    "source": "Windows Event Log (System)",
                    "entries": 50,
                })
        except Exception as e:
            logger.warning("Windows Event Log collectie mislukt: %s", e)
