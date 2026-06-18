from textual.widget import Widget
from textual.app import ComposeResult
from pttm.widgets.timer_widget import TimerWidget
from pttm.widgets.task_list_widget import TaskListWidget

class Dashboard(Widget):
    def compose(self) -> ComposeResult:
        yield TimerWidget(id="timer-widget")
        yield TaskListWidget(id="task-list-widget")
