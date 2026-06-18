from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Label, Static
from textual.reactive import reactive
from pttm.clock import make_clock_ascii
from pttm.config import save_config

MODE_CONFIG_KEYS = {
    "Focus": "focus_time",
    "Short Break": "short_break_time",
    "Long Break": "long_break_time"
}

class TimerWidget(Widget):
    """Widget to display the large digital countdown timer and control panel."""

    mode = reactive("Focus")
    time_remaining = reactive(25 * 60)
    is_running = reactive(False) #type: ignore

    def compose(self) -> ComposeResult:
        yield Label("FOCUS SESSION", id="timer-title")
        yield Label("No task active", id="active-task-display")
        yield Static(id="timer-clock")
        yield Label("Completed: 0 sessions", id="session-count-display")

    def on_mount(self) -> None:
        self.set_interval(1.0, self.tick)

        # Load values from config
        focus_mins = self.app.config["settings"].get("focus_time", 25) #type: ignore
        self.time_remaining = focus_mins * 60
        self.completed_focus_sessions = self.app.config.get("completed_focus_sessions", 0) #type: ignore

        # Force initial display updates
        self.watch_mode(self.mode)
        self.watch_time_remaining(self.time_remaining)
        self.query_one("#session-count-display", Label).update(f"Completed: {self.completed_focus_sessions} sessions")

    def watch_mode(self, mode: str) -> None:
        try:
            title = self.query_one("#timer-title", Label)
            title.update(f"{mode.upper()} SESSION")

            self.remove_class("mode-focus", "mode-short", "mode-long")
            if mode == "Focus":
                self.add_class("mode-focus")
            elif mode == "Short Break":
                self.add_class("mode-short")
            elif mode == "Long Break":
                self.add_class("mode-long")
        except Exception:
            pass

    def watch_time_remaining(self, seconds: int) -> None:
        try:
            self.query_one("#timer-clock", Static).update(make_clock_ascii(seconds))
        except Exception:
            pass

    def tick(self) -> None:
        if self.is_running:
            if self.time_remaining > 0:
                self.time_remaining -= 1
            else:
                self.timer_finished()

    def timer_finished(self) -> None:
        self.is_running = False #type: ignore
        self.update_controls()

        # Terminal visual/audio beep
        print("\a", end="", flush=True)

        self.transition_to_next()

    def transition_to_next(self) -> None:
        if self.mode == "Focus":
            self.completed_focus_sessions += 1
            self.app.config["completed_focus_sessions"] = self.completed_focus_sessions #type: ignore
            save_config(self.app.config) #type: ignore

            self.query_one("#session-count-display", Label).update(f"Completed: {self.completed_focus_sessions} sessions")

            if self.app.active_task_id: #type: ignore
                self.app.increment_active_task_pomodoro() #type: ignore

            interval = self.app.config["settings"].get("long_break_interval", 4) #type: ignore
            if self.completed_focus_sessions % interval == 0:
                self.mode = "Long Break"
                self.app.notify("Focus session completed! Time for a long break.", title="Pomodoro Finished", severity="information")
            else:
                self.mode = "Short Break"
                self.app.notify("Focus session completed! Time for a short break.", title="Pomodoro Finished", severity="information")
        else:
            self.mode = "Focus"
            self.app.notify("Break finished! Time to start focusing.", title="Break Finished", severity="warning")

        self.reset_timer_to_mode()

    def reset_timer_to_mode(self) -> None:
        key = MODE_CONFIG_KEYS[self.mode]
        minutes = self.app.config["settings"].get(key, 25) #type: ignore
        self.time_remaining = minutes * 60
        self.is_running = False #type: ignore
        self.update_controls()

    def update_controls(self) -> None:
        pass
