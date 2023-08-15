from django.core.management.base import BaseCommand

from task.task import task_command


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("command", nargs="*", type=str)

    def handle(self, *args, **options):
        command = options.get("command")
        self.stdout.write(task_command(command))
