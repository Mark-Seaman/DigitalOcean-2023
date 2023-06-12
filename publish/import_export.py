from os import system
from pathlib import Path

from task.models import Activity, Task

from .document import get_document
from .files import read_csv_file, read_json
from .models import Content, Pub
from .toc import content_file, write_content_csv


def create_pubs(pubs):

    def pub_settings(name):
        return read_json(f"static/js/{name}.json")

    def update_record(name, doc_path):
        s = pub_settings(name)
        b = Pub.objects.get_or_create(name=s["name"])[0]
        b.doc_path = s['doc_path']
        b.title = s["site_title"]
        b.subtitle = s["site_subtitle"]
        b.domain = s.get("domain")
        b.url = s["url"]
        b.description = s["description"]
        b.css = s["css"]
        b.image_path = s["image_path"]
        b.cover_image = s.get("cover_image")
        b.pub_type = s.get("pub_type", "blog")
        b.menu = s.get("menu")
        b.logo = s.get("logo")
        b.auto_remove = s.get("auto_remove", False)
        b.auto_index = s.get("auto_index", False)  # simple_index
        b.simple_index = s.get("simple_index", False)
        b.auto_contents = s.get("auto_contents", False)
        b.index_folders = s.get("index_folders", False)
        b.index_months = s.get("index_months", False)
        b.save()
        return b

    def import_pub(pub):
        content = content_file(pub)
        if pub.auto_contents:
            # print("CREATE CONTENT")
            write_content_csv(pub)
        import_content(pub, content)
        delete_extra_objects(pub)

    def set_content(pub, doctype, path, folder, order):
        path = Path(pub.doc_path) / path
        x = Content.objects.get_or_create(
            blog=pub, doctype=doctype, order=order, path=path
        )[0]
        doc = get_document(path)
        x.folder = folder
        x.title = doc["title"]
        x.words = doc["words"]
        x.retain_object = True
        x.save()

    def import_content(pub, index):
        if not index.exists():
            print(f'\n\n***********\nMISSING FILE: {index}\n\n')
        content = read_csv_file(index)
        for row in content:
            if row[2:]:
                set_content(pub, "chapter", row[0], row[1], row[2])
            elif row:
                set_content(pub, "folder", row[0], 0, row[1])
        contents = len(Content.objects.filter(blog=pub))
        # print(f'Contents objects: {pub.name} {contents}')
        assert contents>0

    def delete_extra_objects(pub):
        Content.objects.filter(blog=pub, retain_object=False).delete()
        for c in Content.objects.filter(blog=pub):
            c.retain_object = False
            c.save()

    log = "Create pubs:\n\n"
    for pub in pubs:
        pub = update_record(pub[0], pub[1])
        import_pub(pub)
        log += f"{pub}\n"
    return log


def load_data():
    def reload_pubs():
        Pub.objects.all().delete()
        system("python manage.py loaddata config/publish.json")
        Content.objects.filter(words=0).delete()
        pubs = len(Pub.objects.all())
        print(f"Loaded {pubs} Pubs")
        content = len(Content.objects.all())
        print(f"Loaded {content} Content Posts")

    def reload_tasks():
        Task.objects.all().delete()
        system("python manage.py loaddata config/task.json")
        tasks = len(Task.objects.all())
        print(f"Loaded {tasks} Tasks")
        tasks = len(Activity.objects.all())
        print(f"Loaded {tasks} Activities")

    reload_tasks()
    reload_pubs()


def rename_file(f1, f2):
    if not Path(f1).exists():
        print("No PATH", f1)
    else:
        assert Path(f1).exists()
        Path(f1).rename(Path(f2))
        print(f"rename {f1} {f2}")
    assert Path(f2).exists()


def refresh_pub_from_git():
    system('cd Documents/Shrinking-World-Pubs && git pull')


def save_pub_data():
    command = '''
        {
            python manage.py dumpdata --indent 4 publish > config/publish.json &&
            git add config/publish.json &&
            git commit -m "Save pub JSON" &&
            git push
        } 2>/dev/null  > /dev/null 
    '''
    system(command)
