from django.core.management.base import BaseCommand

from publish.write import write_blog, write_masto, write_review, write_tech, write_words


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("command", nargs="*", type=str)

    def show_usage(self):
        self.stdout.write("usage: write [blog|tech|masto|review|words]")

    def handle(self, *args, **options):
        x = options.get("command")
        if x:
            cmd = x[0]
        else:
            self.show_usage()
            cmd = "blog"

        if cmd == "blog":
            self.stdout.write("WRITE BLOG")
            write_blog(x[1:])

        elif cmd == "tech":
            self.stdout.write("WRITE TECH")
            write_tech(x[1:])

        elif cmd == "masto":
            self.stdout.write("WRITE MASTO")
            write_masto(x[1:])

        elif cmd == "review":
            self.stdout.write("WRITE REVIEW")
            write_review(x[1:])

        elif cmd == "words":
            self.stdout.write("WRITE WORDS")
            write_words(x[1:])

        else:
            self.show_usage()
