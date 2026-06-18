from textual.widget import Widget
from textual.app import ComposeResult
from pmo.widgets.timer_widget import TimerWidget
from pmo.widgets.task_list_widget import TaskListWidget

class Dashboard(Widget):
    def compose(self) -> ComposeResult:
        yield TimerWidget(id="timer-widget")
        yield TaskListWidget(id="task-list-widget")
