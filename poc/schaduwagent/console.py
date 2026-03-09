"""Console-venster — tkinter chat UI voor de eindgebruiker."""

from __future__ import annotations

import tkinter as tk
from datetime import datetime
from threading import Thread
from typing import Callable

from .config import Config


class Console:
    """Eenvoudig chatvenster waarin de gebruiker berichten kan sturen."""

    def __init__(
        self,
        config: Config,
        on_message: Callable[[str], None] | None = None,
        on_stop: Callable[[], None] | None = None,
    ):
        self.config = config
        self._on_message = on_message
        self._on_stop = on_stop
        self._root: tk.Tk | None = None
        self._chat_display: tk.Text | None = None
        self._input_field: tk.Entry | None = None
        self._status_label: tk.Label | None = None
        self._elapsed_label: tk.Label | None = None
        self._get_elapsed: Callable[[], str] | None = None

    def show(self, get_elapsed: Callable[[], str] | None = None):
        """Toon het console-venster. Blokkeert tot het venster gesloten wordt."""
        self._get_elapsed = get_elapsed
        self._root = tk.Tk()
        self._root.title(self.config.console_title)
        self._root.geometry(f"{self.config.console_width}x{self.config.console_height}")
        self._root.configure(bg="#1e1e2e")
        self._root.resizable(True, True)

        self._build_ui()
        self._add_agent_message("Sessie gestart. De servicedesk kan nu meekijken.")
        self._update_elapsed()
        self._root.mainloop()

    def show_in_thread(self, get_elapsed: Callable[[], str] | None = None):
        """Toon het console-venster in een achtergrondthread."""
        t = Thread(target=self.show, args=(get_elapsed,), daemon=True, name="console")
        t.start()
        return t

    def _build_ui(self):
        """Bouwt de UI-componenten."""
        root = self._root

        # Header met status en timer
        header = tk.Frame(root, bg="#313244", padx=10, pady=8)
        header.pack(fill=tk.X)

        title = tk.Label(
            header, text="Schaduwagent", font=("Segoe UI", 12, "bold"),
            fg="#cdd6f4", bg="#313244",
        )
        title.pack(side=tk.LEFT)

        self._status_label = tk.Label(
            header, text=" ● Sessie actief", font=("Segoe UI", 10),
            fg="#a6e3a1", bg="#313244",
        )
        self._status_label.pack(side=tk.LEFT, padx=(10, 0))

        self._elapsed_label = tk.Label(
            header, text="00:00:00", font=("Consolas", 10),
            fg="#bac2de", bg="#313244",
        )
        self._elapsed_label.pack(side=tk.RIGHT)

        # Chat display
        chat_frame = tk.Frame(root, bg="#1e1e2e")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 0))

        self._chat_display = tk.Text(
            chat_frame, wrap=tk.WORD, state=tk.DISABLED,
            bg="#1e1e2e", fg="#cdd6f4", font=("Consolas", 10),
            borderwidth=0, highlightthickness=0, padx=8, pady=8,
            selectbackground="#45475a",
        )
        scrollbar = tk.Scrollbar(chat_frame, command=self._chat_display.yview)
        self._chat_display.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Text tags voor kleuren
        self._chat_display.tag_config("agent", foreground="#89b4fa")
        self._chat_display.tag_config("user", foreground="#a6e3a1")
        self._chat_display.tag_config("time", foreground="#6c7086")
        self._chat_display.tag_config("system", foreground="#f9e2af")

        # Input frame
        input_frame = tk.Frame(root, bg="#313244", padx=10, pady=8)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Stop knop
        stop_btn = tk.Button(
            input_frame, text="Stop sessie", font=("Segoe UI", 9),
            bg="#f38ba8", fg="#1e1e2e", activebackground="#eba0ac",
            borderwidth=0, padx=12, pady=4, command=self._handle_stop,
        )
        stop_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Verstuur knop
        send_btn = tk.Button(
            input_frame, text=">", font=("Segoe UI", 11, "bold"),
            bg="#89b4fa", fg="#1e1e2e", activebackground="#b4befe",
            borderwidth=0, width=3, pady=2, command=self._handle_send,
        )
        send_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Invoerveld
        self._input_field = tk.Entry(
            input_frame, font=("Consolas", 10),
            bg="#45475a", fg="#cdd6f4", insertbackground="#cdd6f4",
            borderwidth=0, highlightthickness=1, highlightcolor="#89b4fa",
        )
        self._input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        self._input_field.bind("<Return>", lambda e: self._handle_send())
        self._input_field.focus_set()

    def _handle_send(self):
        """Verwerkt een bericht van de gebruiker."""
        if not self._input_field:
            return
        text = self._input_field.get().strip()
        if not text:
            return
        self._input_field.delete(0, tk.END)
        self._add_user_message(text)
        if self._on_message:
            self._on_message(text)

    def _handle_stop(self):
        """Stopt de sessie."""
        self._add_system_message("Sessie wordt gestopt...")
        if self._status_label:
            self._status_label.config(text=" ● Gestopt", fg="#f38ba8")
        if self._on_stop:
            self._on_stop()
        if self._root:
            self._root.after(1000, self._root.destroy)

    def _add_message(self, prefix: str, text: str, tag: str):
        """Voegt een bericht toe aan de chat display."""
        if not self._chat_display:
            return
        self._chat_display.config(state=tk.NORMAL)
        now = datetime.now().strftime("%H:%M:%S")
        self._chat_display.insert(tk.END, f"[{now}] ", "time")
        self._chat_display.insert(tk.END, f"[{prefix}] ", tag)
        self._chat_display.insert(tk.END, f"{text}\n\n", tag)
        self._chat_display.config(state=tk.DISABLED)
        self._chat_display.see(tk.END)

    def _add_agent_message(self, text: str):
        self._add_message("Agent", text, "agent")

    def _add_user_message(self, text: str):
        self._add_message("Jij", text, "user")

    def _add_system_message(self, text: str):
        self._add_message("Systeem", text, "system")

    def add_agent_response(self, text: str):
        """Voegt een agent-bericht toe (thread-safe via after())."""
        if self._root:
            self._root.after(0, lambda: self._add_agent_message(text))

    def _update_elapsed(self):
        """Update de verstreken tijd elke seconde."""
        if self._get_elapsed and self._elapsed_label:
            self._elapsed_label.config(text=self._get_elapsed())
        if self._root:
            self._root.after(1000, self._update_elapsed)
