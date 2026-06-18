import json
import os
from textual.app import App, ComposeResult
from textual.widgets import Header, TabbedContent, TabPane, Label, Input
from pttm.config import load_config, save_config
from pttm.widgets.dashboard import Dashboard
from pttm.widgets.settings_tab import SettingsTab
from pttm.widgets.shortcuts_screen import ShortcutsScreen
from pttm.widgets.timer_widget import TimerWidget
from pttm.widgets.task_list_widget import TaskListWidget

class PomodoroApp(App):
    CSS_PATH = "pmo.css"
    TITLE = "TS PMO"
    COMMANDS = set()
    ENABLE_COMMAND_PALETTE = False

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "toggle_timer", "Start/Pause"),
        ("r", "reset_timer", "Reset"),
        ("ctrl+r", "reset_session", "Reset Session"),
        ("k", "skip_timer", "Skip"),
        ("f", "set_mode_focus", "Focus Mode"),
        ("g", "set_mode_short", "Short Break"),
        ("b", "set_mode_long", "Long Break"),
        ("t", "focus_todo_input", "Focus Todo"),
        ("ctrl+p", "toggle_shortcuts", "Shortcuts"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = load_config()
        # Log config to startup file next to config file
        from pttm.config import CONFIG_FILE
        log_dir = os.path.dirname(CONFIG_FILE)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "pmo_startup.log")
        else:
            log_file = "pmo_startup.log"
        try:
            with open(log_file, "w") as f:
                f.write(json.dumps(self.config, indent=4))
        except Exception:
            pass
        self.active_task_id = None

    def compose(self) -> ComposeResult:
        # yield Header(show_clock=True)
        with TabbedContent(initial="timer-tab"):
            with TabPane("Timer", id="timer-tab"):
                yield TimerWidget()
            with TabPane("Tasks", id="tasks-tab"):
                yield TaskListWidget()
            with TabPane("Settings", id="settings-tab"):
                yield SettingsTab()

    def action_toggle_timer(self) -> None:
        try:
            timer_widget = self.query_one(TimerWidget)
            timer_widget.is_running = not timer_widget.is_running #type: ignore
        except Exception:
            pass

    def action_reset_timer(self) -> None:
        try:
            timer_widget = self.query_one(TimerWidget)
            timer_widget.reset_timer_to_mode()
        except Exception:
            pass

    def action_skip_timer(self) -> None:
        try:
            timer_widget = self.query_one(TimerWidget)
            timer_widget.transition_to_next()
        except Exception:
            pass

    def action_set_mode_focus(self) -> None:
        try:
            timer_widget = self.query_one(TimerWidget)
            timer_widget.mode = "Focus"
            timer_widget.reset_timer_to_mode()
        except Exception:
            pass

    def action_set_mode_short(self) -> None:
        try:
            timer_widget = self.query_one(TimerWidget)
            timer_widget.mode = "Short Break"
            timer_widget.reset_timer_to_mode()
        except Exception:
            pass

    def action_set_mode_long(self) -> None:
        try:
            timer_widget = self.query_one(TimerWidget)
            timer_widget.mode = "Long Break"
            timer_widget.reset_timer_to_mode()
        except Exception:
            pass

    def action_focus_todo_input(self) -> None:
        try:
            input_box = self.query_one("#new-task-input", Input)
            input_box.focus()
        except Exception:
            pass

    def action_toggle_shortcuts(self) -> None:
        if isinstance(self.screen, ShortcutsScreen):
            self.pop_screen()
        else:
            self.push_screen(ShortcutsScreen())

    def action_reset_session(self) -> None:
        try:
            timer_widget = self.query_one(TimerWidget)
            timer_widget.is_running = False #type: ignore
            timer_widget.completed_focus_sessions = 0
            self.config["completed_focus_sessions"] = 0
            save_config(self.config)

            timer_widget.query_one("#session-count-display", Label).update("Completed: 0 sessions")
            timer_widget.mode = "Focus"
            timer_widget.reset_timer_to_mode()
            self.notify("Pomodoro session reset completely.", title="Session Reset", severity="information")
        except Exception:
            pass

    def update_active_task_display(self) -> None:
        try:
            timer_widget = self.query_one(TimerWidget)
            active_label = timer_widget.query_one("#active-task-display", Label)

            active_task = None
            if self.active_task_id:
                for task in self.config.get("tasks", []):
                    if task["id"] == self.active_task_id:
                        active_task = task
                        break

            if active_task:
                active_label.update(f"Active Task: [bold #f9e2af]{active_task['title']}[/bold #f9e2af]")
                timer_widget.query_one("#timer-clock").add_class("timer-clock-active")
            else:
                active_label.update("No active task selected")
                timer_widget.query_one("#timer-clock").remove_class("timer-clock-active")
        except Exception:
            pass

    def increment_active_task_pomodoro(self) -> None:
        if not self.active_task_id:
            return

        for task in self.config["tasks"]:
            if task["id"] == self.active_task_id:
                task["pomodoros"] += 1
                self.notify(f"Pomodoro recorded for: {task['title']}", title="Task Updated", severity="success") #type: ignore
                break
        save_config(self.config)

        try:
            task_list_widget = self.query_one(TaskListWidget)
            task_list_widget.refresh_tasks()
        except Exception:
            pass

    def on_settings_updated(self) -> None:
        try:
            timer_widget = self.query_one(TimerWidget)
            if not timer_widget.is_running:
                timer_widget.reset_timer_to_mode()
        except Exception:
            pass

def main():
    app = PomodoroApp()
    app.run()

if __name__ == "__main__":
    main()
