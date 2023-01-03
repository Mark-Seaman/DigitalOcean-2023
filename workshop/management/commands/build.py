from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from course.import_export import import_all_courses
from course.textbook import generate_textbook
from publish.import_export import load_data
from publish.pub import build_pubs
from publish.seamanslog import review_file
from workshop.imager import build_images, build_logos


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("command", nargs="*", type=str)

    def handle(self, *args, **options):
        x = options.get("command")
        if not x:
            print(
                """Build Options: courses, data, webapps, images, logos, review tasks"""
            )
            return

        cmd = x[0]
        if cmd == "data":
            print("BUILD DATA")
            load_data()
        elif cmd == "courses":
            print("BUILD COURSES")
            print(import_all_courses())
        elif cmd == "images":
            print("BUILD IMAGES")
            print(build_images())
        elif cmd == "logos":
            print("BUILD LOGOS")
            print(build_logos())
        elif cmd == "pubs":
            print("BUILD PUBS")
            print(build_pubs())
        elif cmd == "review":
            review_file()
        elif cmd == "user":
            get_user_model().objects.get(username="seaman").delete()
            user_args = dict(
                username="seaman",
                email="mark.seaman@shrinking-world.com",
                password="MS1959-sws",
            )
            get_user_model().objects.create_user(**user_args)
        elif cmd == "webapps":
            print("BUILD WEB APPS BOOK")
            generate_textbook()
        else:
            print(
                """Build Options: books, courses, data, webapps, images, logos, tasks"""
            )
