"""System tray integratie — pictogram naast de klok met start/stop/console."""

from __future__ import annotations

import logging
from threading import Thread
from typing import Callable

from PIL import Image, ImageDraw

logger = logging.getLogger(__name__)


def _create_icon_image(color: str = "#a6e3a1", size: int = 64) -> Image.Image:
    """Maakt een eenvoudig tray-icoon: een gevulde cirkel."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    margin = size // 8
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=color,
        outline="#313244",
        width=2,
    )
    return img


class TrayIcon:
    """System tray icoon met menu voor start/stop sessie en console."""

    def __init__(
        self,
        on_start: Callable[[], None] | None = None,
        on_stop: Callable[[], None] | None = None,
        on_console: Callable[[], None] | None = None,
        on_quit: Callable[[], None] | None = None,
    ):
        self._on_start = on_start
        self._on_stop = on_stop
        self._on_console = on_console
        self._on_quit = on_quit
        self._icon = None
        self._active = False

    def run(self):
        """Start het tray-icoon. Blokkeert tot het icoon gestopt wordt."""
        try:
            import pystray
            from pystray import MenuItem as Item

            menu = pystray.Menu(
                Item("Start sessie", self._handle_start, visible=lambda item: not self._active),
                Item("Stop sessie", self._handle_stop, visible=lambda item: self._active),
                Item("Open console", self._handle_console),
                pystray.Menu.SEPARATOR,
                Item("Afsluiten", self._handle_quit),
            )

            self._icon = pystray.Icon(
                "schaduwagent",
                icon=_create_icon_image("#6c7086"),  # Grijs = inactief
                title="Schaduwagent (inactief)",
                menu=menu,
            )
            self._icon.run()
        except Exception as e:
            logger.warning("System tray niet beschikbaar: %s. Draai zonder tray.", e)

    def run_in_thread(self) -> Thread:
        """Start het tray-icoon in een achtergrondthread."""
        t = Thread(target=self.run, daemon=True, name="tray")
        t.start()
        return t

    def set_active(self, active: bool):
        """Update het tray-icoon naar actief/inactief."""
        self._active = active
        if self._icon:
            if active:
                self._icon.icon = _create_icon_image("#a6e3a1")  # Groen
                self._icon.title = "Schaduwagent (sessie actief)"
            else:
                self._icon.icon = _create_icon_image("#6c7086")  # Grijs
                self._icon.title = "Schaduwagent (inactief)"

    def stop(self):
        """Stopt het tray-icoon."""
        if self._icon:
            self._icon.stop()

    def _handle_start(self, icon, item):
        if self._on_start:
            self._on_start()

    def _handle_stop(self, icon, item):
        if self._on_stop:
            self._on_stop()

    def _handle_console(self, icon, item):
        if self._on_console:
            self._on_console()

    def _handle_quit(self, icon, item):
        if self._on_quit:
            self._on_quit()
