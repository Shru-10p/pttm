import uuid
from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Label, Input
from textual.containers import Horizontal, VerticalScroll
from textual import events
from pttm.widgets.task_item import TaskItem
from pttm.config import save_config

class TaskListWidget(Widget):
    """Widget to display the todo list and manage tasks."""

    def compose(self) -> ComposeResult:
        yield Label("TASK LIST", id="todo-title")

        with Horizontal(id="todo-input-row"):
            yield Input(placeholder="Add a new task...", id="new-task-input")

        yield VerticalScroll(id="tasks-container")
        # yield Label("Space: check | Enter/f: focus | e: edit | d: delete", id="todo-help")

    def on_mount(self) -> None:
        self.refresh_tasks()

    def refresh_tasks(self) -> None:
        container = self.query_one("#tasks-container")

        # Clear existing tasks
        for child in list(container.children):
            child.remove()

        # Add tasks from app config
        for task in self.app.config.get("tasks", []): #type: ignore
            is_active = (task["id"] == self.app.active_task_id) #type: ignore
            task_item = TaskItem(
                task_id=task["id"],
                title=task["title"],
                completed=task["completed"],
                pomodoros=task["pomodoros"],
                is_active=is_active
            )
            container.mount(task_item)

            if is_active:
                task_item.add_class("active-task")

    def on_task_item_toggle(self, event: TaskItem.Toggle) -> None:
        for task in self.app.config["tasks"]: #type: ignore
            if task["id"] == event.task_item.task_id:
                task["completed"] = event.completed
                break
        save_config(self.app.config) #type: ignore

    def on_task_item_select(self, event: TaskItem.Select) -> None:
        if self.app.active_task_id == event.task_item.task_id: #type: ignore
            self.app.active_task_id = None #type: ignore
        else:
            self.app.active_task_id = event.task_item.task_id #type: ignore

        self.app.update_active_task_display() #type: ignore
        self.refresh_tasks()
        self.query_one("#new-task-input", Input).focus()


    def on_task_item_delete(self, event: TaskItem.Delete) -> None:
        if self.app.active_task_id == event.task_item.task_id: #type: ignore
            self.app.active_task_id = None #type: ignore

        self.app.config["tasks"] = [t for t in self.app.config["tasks"] if t["id"] != event.task_item.task_id] #type: ignore
        save_config(self.app.config) #type: ignore

        self.app.update_active_task_display() #type: ignore
        self.refresh_tasks()
        self.query_one("#new-task-input", Input).focus()

    def on_task_item_rename(self, event: TaskItem.Rename) -> None:
        for task in self.app.config["tasks"]: #type: ignore
            if task["id"] == event.task_item.task_id:
                task["title"] = event.new_title
                break
        save_config(self.app.config) #type: ignore

        if self.app.active_task_id == event.task_item.task_id: #type: ignore
            self.app.update_active_task_display() #type: ignore

    def add_task(self) -> None:
        input_widget = self.query_one("#new-task-input", Input)
        title = input_widget.value.strip()
        if not title:
            return

        new_task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "completed": False,
            "pomodoros": 0
        }

        self.app.config.setdefault("tasks", []) #type: ignore
        self.app.config["tasks"].append(new_task) #type: ignore
        save_config(self.app.config) #type: ignore

        input_widget.value = ""
        self.refresh_tasks()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "new-task-input":
            self.add_task()

    def on_key(self, event: events.Key) -> None:
        """Down arrow on the add-task input jumps to the first task item."""
        if event.key == "down" and self.focused_child_is_input():
            items = list(self.query(TaskItem))
            if items:
                event.stop()
                items[0].focus()

    def focused_child_is_input(self) -> bool:
        """Return True when the new-task Input currently has focus."""
        try:
            return self.query_one("#new-task-input", Input).has_focus
        except Exception:
            return False
