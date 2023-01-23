from django.core.management.base import BaseCommand

from task.task import import_tasks, show_task_summary


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("command", nargs="*", type=str)

    def show_usage(self):
        self.stdout.write("usage: write [blog|tech|masto|review|words]")

    def handle(self, *args, **options):
        x = options.get("command")
        if not x:
            days = 1
        elif x[0] == 'day':
            days = 1
        elif x[0] == 'week':
            days = 8
        elif x[0] == 'month':
            days = 31
        elif x[0] == 'year':
            days = 366
        else:
            days = None
        if days:
            import_tasks()
            text = show_task_summary(days=days)
            if text:
                self.stdout.write(text)
