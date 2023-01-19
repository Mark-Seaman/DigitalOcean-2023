from django.core.management.base import BaseCommand

from task.task import show_task_summary


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("command", nargs="*", type=str)

    def show_usage(self):
        self.stdout.write("usage: write [blog|tech|masto|review|words]")

    def handle(self, *args, **options):
        x = options.get("command")
        text = show_task_summary(days=31)
        if text:
            self.stdout.write(text)
