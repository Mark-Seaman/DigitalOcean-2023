from django.core.management.base import BaseCommand

from writer.pub_script import pub_script


class Command(BaseCommand):
    help = 'Execute a script that is passed as a list of words.'

    def add_arguments(self, parser):
        parser.add_argument('command_args', nargs='+', type=str)

    def handle(self, *args, **options):
        command_args = options['command_args']
        output = pub_script(command_args)
        if output:
            self.stdout.write(output)
