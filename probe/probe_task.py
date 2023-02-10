from publish.days import recent_dates
from publish.text import text_join
from task.models import Task
from task.task import show_task_summary, task_import_files, time_summary, time_table


def test_task_recent():
    return text_join(recent_dates(30))


def test_task_records():
    task_import_files(30)
    return f'TASK RECORDS: {len(Task.objects.all())}'


def test_task_summary():
    return time_summary()


def test_task_time():
    return show_task_summary()
