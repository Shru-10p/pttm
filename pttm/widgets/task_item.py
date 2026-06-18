from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Label, Input
from textual.message import Message
from textual import events

class TaskItem(Widget):
    """A widget representing a single task item."""
    
    can_focus = True
    
    class Toggle(Message):
        def __init__(self, task_item: "TaskItem", completed: bool):
            super().__init__()
            self.task_item = task_item
            self.completed = completed
            
    class Select(Message):
        def __init__(self, task_item: "TaskItem"):
            super().__init__()
            self.task_item = task_item
            
    class Delete(Message):
        def __init__(self, task_item: "TaskItem"):
            super().__init__()
            self.task_item = task_item

    class Rename(Message):
        def __init__(self, task_item: "TaskItem", new_title: str):
            super().__init__()
            self.task_item = task_item
            self.new_title = new_title

    def __init__(self, task_id: str, title: str, completed: bool, pomodoros: int, is_active: bool = False):
        super().__init__()
        self.task_id = task_id
        self.title = title
        self.completed = completed
        self.pomodoros = pomodoros
        self.is_active = is_active

    def compose(self) -> ComposeResult:
        check_char = "[x]" if self.completed else "[ ]"
        yield Label(check_char, classes="task-check-lbl")
        
        title_cls = "task-title completed" if self.completed else "task-title"
        yield Label(self.title, classes=title_cls)
        yield Input(value=self.title, classes="task-edit-input hidden")
        
        yield Label(f"({self.pomodoros})", classes="task-pomo")

    def on_key(self, event: events.Key) -> None:
        key = event.key
        if key == "space":
            event.stop()
            self.completed = not self.completed
            self.post_message(self.Toggle(self, self.completed))
            self.refresh_task_display()
        elif key == "e":
            event.stop()
            self.start_editing()
        elif key == "d":
            event.stop()
            self.post_message(self.Delete(self))
        elif key in ("enter", "f"):
            event.stop()
            self.post_message(self.Select(self))

    def refresh_task_display(self) -> None:
        try:
            check_lbl = self.query_one(".task-check-lbl", Label)
            check_lbl.update("[x]" if self.completed else "[ ]")
            title_lbl = self.query_one(".task-title", Label)
            if self.completed:
                title_lbl.add_class("completed")
            else:
                title_lbl.remove_class("completed")
        except Exception:
            pass

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if "task-edit-input" in event.input.classes:
            event.stop()
            self.save_edit()

    def start_editing(self) -> None:
        try:
            self.query_one(".task-title", Label).add_class("hidden")
            edit_input = self.query_one(".task-edit-input", Input)
            edit_input.remove_class("hidden")
            edit_input.focus()
        except Exception:
            pass

    def save_edit(self) -> None:
        try:
            edit_input = self.query_one(".task-edit-input", Input)
            new_title = edit_input.value.strip()
            if new_title:
                self.title = new_title
                label = self.query_one(".task-title", Label)
                label.update(self.title)
                self.post_message(self.Rename(self, self.title))
                
            self.query_one(".task-title", Label).remove_class("hidden")
            edit_input.add_class("hidden")
            self.focus()
        except Exception:
            pass
