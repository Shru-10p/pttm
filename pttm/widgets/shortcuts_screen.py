from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Label

class ShortcutsScreen(ModalScreen):
    BINDINGS = [
        ("escape", "dismiss_dialog", "Close"),
        ("ctrl+p", "dismiss_dialog", "Close"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="shortcuts-dialog"):
            yield Label("KEYBOARD SHORTCUTS", id="shortcuts-title")

            with VerticalScroll(id="shortcuts-content"):
                yield Label("[bold]Global Controls[/bold]", classes="section-header")
                yield Label("  q                - Quit App", classes="shortcut-entry")
                yield Label("  Space / s        - Start / Pause Timer", classes="shortcut-entry")
                yield Label("  r                - Reset Timer", classes="shortcut-entry")
                yield Label("  Ctrl+R           - Reset Entire Session", classes="shortcut-entry")
                yield Label("  k                - Skip Session", classes="shortcut-entry")
                yield Label("  f                - Switch to Focus Session", classes="shortcut-entry")
                yield Label("  g                - Switch to Short Break", classes="shortcut-entry")
                yield Label("  b                - Switch to Long Break", classes="shortcut-entry")
                yield Label("  t                - Focus Todo Creation Box", classes="shortcut-entry")
                yield Label("  Ctrl+P           - Toggle Keyboard Shortcuts", classes="shortcut-entry")
                yield Label("  Esc              - Focus tab bar (Tasks/Settings)", classes="shortcut-entry")

                yield Label("", classes="spacer")
                yield Label("[bold]Todo Checklist Controls[/bold]", classes="section-header")
                yield Label("  ↑ / ↓            - Navigate between tasks", classes="shortcut-entry")
                yield Label("  Esc              - Return to task input box", classes="shortcut-entry")
                yield Label("  Tab              - Navigate through checklist", classes="shortcut-entry")
                yield Label("  Space / Enter    - Toggle task completion", classes="shortcut-entry")
                yield Label("  f                - Set task as active target", classes="shortcut-entry")
                yield Label("  e                - Rename task title inline", classes="shortcut-entry")
                yield Label("  d                - Delete task from checklist", classes="shortcut-entry")

                yield Label("", classes="spacer")
                yield Label("[bold]Settings Controls[/bold]", classes="section-header")
                yield Label("  ↑ / ↓            - Navigate between fields", classes="shortcut-entry")

            yield Label("[ Close [esc] ]", id="shortcuts-close-btn")

    def action_dismiss_dialog(self) -> None:
        self.dismiss()
