from publish.days import recent_dates
from publish.text import text_join
from task.models import Task
from task.task import fix_tasks, task_command


def test_task_recent():
    return text_join(recent_dates(30))


def test_task_records():
    return task_command(['week', '2023-02-01', 'activity'])


def test_task_fix():
    fix_tasks()
    return 'OK'
