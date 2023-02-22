from publish.days import recent_dates
from publish.text import text_join
from task.models import Task
from task.task import (fix_tasks, show_task_summary, task_command, task_import_files,
                       time_summary)


def test_task_recent():
    return text_join(recent_dates(30))


def test_task_records():
    text = task_command(['week'])
    return f'Week: {text}\n\nTASK RECORDS: {len(Task.objects.all())}'


def test_task_fix():
    fix_tasks()
    return 'OK'


def test_task_summary():
    return time_summary(days=31)


def test_task_time():
    return show_task_summary(days=7)
