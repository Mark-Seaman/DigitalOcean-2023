from io import StringIO
from pathlib import Path
from django.core.management import call_command

from publish.models import Pub


def save_json_data(file, app=None):
    # output = StringIO()
    if app:
        call_command('dumpdata', app, indent=4, output=file)
    else:
        call_command('dumpdata', indent=4, output=file,
                     exclude=['contenttypes'])
    # text = output.getvalue()
    # output.close()
    # Path(file).write_text(text)
    return Path(file).read_text()


def load_json_data(file):
    output = StringIO()
    call_command('loaddata', file, stdout=output)
    text = output.getvalue()
    output.close()
    return text


# -----------


# def load_data():
#     Pub.objects.all().delete()
#     system("python manage.py loaddata config/publish.json")
#     Content.objects.filter(words=0).delete()
#     pubs = len(Pub.objects.all())
#     print(f"Loaded {pubs} Pubs")
#     content = len(Content.objects.all())
#     print(f"Loaded {content} Content Posts")


# def save_pub_data():
#     command = '''
#         {
#             python manage.py dumpdata --indent 4 publish > config/publish.json &&
#             git add config/publish.json &&
#             git commit -m "Save pub JSON" &&
#             git push
#         } 2>/dev/null  > /dev/null
#     '''
#     system(command)


# def save_json_data(file, app=None):
#     output = StringIO()
#     if app:
#         call_command('dumpdata', app, stdout=output, indent=4)
#     else:
#         call_command('dumpdata', stdout=output, indent=4)
#     text = output.getvalue()
#     output.close()
#     Path(file).write_text(text)
#     return text


# def load_json_data(file):
#     output = StringIO()
#     call_command('loaddata', file, stdout=output)
#     text = output.getvalue()
#     output.close()
#     return text
