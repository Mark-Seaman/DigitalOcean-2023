from task.models import Task
from task.task import task_import_files, time_summary, time_table


def test_task_records():
    task_import_files(30)
    return f'TASK RECORDS: {len(Task.objects.all())}'


def test_task_summary():
    return time_summary()
