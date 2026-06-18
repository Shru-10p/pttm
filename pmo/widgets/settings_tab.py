from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button
from textual.containers import Horizontal, VerticalScroll
from pmo.config import save_config

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

            yield Button("[apply & save]", id="save-settings-btn")
            yield Label("", id="settings-status")

    def on_mount(self) -> None:
        config = self.app.config.get("settings", {}) #type: ignore
        self.query_one("#setting-focus", Input).value = str(config.get("focus_time", 25))
        self.query_one("#setting-short", Input).value = str(config.get("short_break_time", 5))
        self.query_one("#setting-long", Input).value = str(config.get("long_break_time", 15))
        self.query_one("#setting-interval", Input).value = str(config.get("long_break_interval", 4))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-settings-btn":
            try:
                focus_time = int(self.query_one("#setting-focus", Input).value)
                short_break = int(self.query_one("#setting-short", Input).value)
                long_break = int(self.query_one("#setting-long", Input).value)
                interval = int(self.query_one("#setting-interval", Input).value)

                if focus_time <= 0 or short_break <= 0 or long_break <= 0 or interval <= 0:
                    raise ValueError("All values must be positive integers.")

                self.app.config["settings"] = { #type: ignore
                    "focus_time": focus_time,
                    "short_break_time": short_break,
                    "long_break_time": long_break,
                    "long_break_interval": interval
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
