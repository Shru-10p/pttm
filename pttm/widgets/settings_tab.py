from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Switch
from textual.containers import Horizontal, VerticalScroll
from textual import events
from pttm.config import save_config

# Ordered list of focusable settings field IDs — used for arrow-key cycling.
_FIELD_ORDER = [
    "setting-focus",
    "setting-short",
    "setting-long",
    "setting-interval",
    "setting-auto-start",
    "save-settings-btn",
]

class SettingsTab(Widget):
    def compose(self) -> ComposeResult:
        with VerticalScroll(id="settings-form"):
            yield Label("POMODORO SETTINGS", classes="settings-title")

            with Horizontal(classes="settings-row"):
                yield Label("Focus Session (mins):", classes="settings-label")
                yield Input(placeholder="25", id="setting-focus", restrict=r"^[0-9]*$")

            with Horizontal(classes="settings-row"):
                yield Label("Short Break (mins):", classes="settings-label")
                yield Input(placeholder="5", id="setting-short", restrict=r"^[0-9]*$")

            with Horizontal(classes="settings-row"):
                yield Label("Long Break (mins):", classes="settings-label")
                yield Input(placeholder="15", id="setting-long", restrict=r"^[0-9]*$")

            with Horizontal(classes="settings-row"):
                yield Label("Sessions before Long Break:", classes="settings-label")
                yield Input(placeholder="4", id="setting-interval", restrict=r"^[0-9]*$")

            with Horizontal(classes="settings-row settings-row-switch"):
                yield Label("Auto-start next session:", classes="settings-label")
                yield Switch(id="setting-auto-start", value=False)

            yield Button("[apply & save]", id="save-settings-btn")
            yield Label("", id="settings-status")

    def on_mount(self) -> None:
        config = self.app.config.get("settings", {}) #type: ignore
        self.query_one("#setting-focus", Input).value = str(config.get("focus_time", 25))
        self.query_one("#setting-short", Input).value = str(config.get("short_break_time", 5))
        self.query_one("#setting-long", Input).value = str(config.get("long_break_time", 15))
        self.query_one("#setting-interval", Input).value = str(config.get("long_break_interval", 4))
        self.query_one("#setting-auto-start", Switch).value = bool(config.get("auto_start_next", False))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-settings-btn":
            try:
                focus_time = int(self.query_one("#setting-focus", Input).value)
                short_break = int(self.query_one("#setting-short", Input).value)
                long_break = int(self.query_one("#setting-long", Input).value)
                interval = int(self.query_one("#setting-interval", Input).value)
                auto_start = self.query_one("#setting-auto-start", Switch).value

                if focus_time <= 0 or short_break <= 0 or long_break <= 0 or interval <= 0:
                    raise ValueError("All values must be positive integers.")

                self.app.config["settings"] = { #type: ignore
                    "focus_time": focus_time,
                    "short_break_time": short_break,
                    "long_break_time": long_break,
                    "long_break_interval": interval,
                    "auto_start_next": auto_start
                }
                save_config(self.app.config) #type: ignore

                status_label = self.query_one("#settings-status", Label)
                status_label.update("[OK] Settings saved successfully!")
                status_label.styles.color = "#a6e3a1"

                self.app.on_settings_updated() #type: ignore
            except ValueError as e:
                status_label = self.query_one("#settings-status", Label)
                status_label.update(f"[Error] {str(e)}")
                status_label.styles.color = "#f38ba8"

    def on_key(self, event: events.Key) -> None:
        """Navigate between settings fields with Up / Down arrows."""
        if event.key not in ("up", "down"):
            return

        # Find which field currently has focus
        focused_id: str | None = None
        for field_id in _FIELD_ORDER:
            try:
                widget = self.query_one(f"#{field_id}")
                if widget.has_focus:
                    focused_id = field_id
                    break
            except Exception:
                pass

        if focused_id is None:
            return

        event.stop()
        idx = _FIELD_ORDER.index(focused_id)
        if event.key == "down":
            next_id = _FIELD_ORDER[(idx + 1) % len(_FIELD_ORDER)]
        else:
            next_id = _FIELD_ORDER[(idx - 1) % len(_FIELD_ORDER)]

        try:
            self.query_one(f"#{next_id}").focus()
        except Exception:
            pass
