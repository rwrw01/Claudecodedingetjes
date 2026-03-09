"""Sessiebeheer — maakt sessie-mappen aan en schrijft JSONL events."""

from __future__ import annotations

import json
import platform
import socket
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

from .config import Config


class Session:
    """Beheert een enkele schaduwagent-sessie met JSONL event-stream."""

    def __init__(self, config: Config):
        self.config = config
        self._lock = Lock()
        self._active = False
        self._start_time: datetime | None = None
        self.session_dir: Path | None = None
        self._events_file: Path | None = None
        self._messages_file: Path | None = None
        self._event_counter = 0
        self._screenshot_counter = 0

    @property
    def active(self) -> bool:
        return self._active

    @property
    def elapsed(self) -> str:
        """Geeft verstreken sessietijd als HH:MM:SS string."""
        if not self._start_time:
            return "00:00:00"
        delta = datetime.now(timezone.utc) - self._start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def start(self) -> Path:
        """Start een nieuwe sessie. Retourneert het sessie-pad."""
        now = datetime.now()
        session_name = now.strftime("%Y-%m-%d_%H%M%S")
        self.session_dir = self.config.sessie_root / session_name
        self.session_dir.mkdir(parents=True, exist_ok=True)
        (self.session_dir / "screenshots").mkdir(exist_ok=True)
        (self.session_dir / "logs").mkdir(exist_ok=True)

        self._events_file = self.session_dir / "events.jsonl"
        self._messages_file = self.session_dir / "user_messages.jsonl"
        self._event_counter = 0
        self._screenshot_counter = 0
        self._start_time = datetime.now(timezone.utc)
        self._active = True

        # Schrijf session_start event
        self.write_event("session_start", {
            "hostname": socket.gethostname(),
            "os": f"{platform.system()} {platform.release()}",
            "os_version": platform.version(),
            "machine": platform.machine(),
            "session_dir": str(self.session_dir),
        })

        return self.session_dir

    def stop(self):
        """Stopt de actieve sessie."""
        if self._active:
            self.write_event("session_stop", {"elapsed": self.elapsed})
            self._active = False

    def write_event(self, event_type: str, data: dict | None = None) -> dict:
        """Schrijft een event naar events.jsonl. Thread-safe."""
        event = {
            "ts": datetime.now(timezone.utc).strftime("%H:%M:%S"),
            "ts_iso": datetime.now(timezone.utc).isoformat(),
            "seq": self._event_counter,
            "type": event_type,
        }
        if data:
            event.update(data)

        with self._lock:
            self._event_counter += 1
            if self._events_file:
                with open(self._events_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(event, ensure_ascii=False) + "\n")

        return event

    def write_user_message(self, text: str) -> dict:
        """Schrijft een gebruikersbericht naar user_messages.jsonl en events.jsonl."""
        msg = {
            "ts": datetime.now(timezone.utc).strftime("%H:%M:%S"),
            "ts_iso": datetime.now(timezone.utc).isoformat(),
            "text": text,
        }

        with self._lock:
            if self._messages_file:
                with open(self._messages_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(msg, ensure_ascii=False) + "\n")

        self.write_event("user_message", {"text": text})
        return msg

    def next_screenshot_path(self, trigger: str = "periodic") -> Path:
        """Genereert het volgende screenshot pad."""
        self._screenshot_counter += 1
        filename = f"screen_{self._screenshot_counter:03d}.png"
        return self.session_dir / "screenshots" / filename

    def write_log_file(self, name: str, content: str):
        """Schrijft een logbestand naar de logs/ map."""
        if self.session_dir:
            log_path = self.session_dir / "logs" / name
            log_path.write_text(content, encoding="utf-8")
