from os import system
from pathlib import Path

from task.models import Activity, Task

from .document import get_document
from .files import read_csv_file, read_json
from .models import Content, Pub
from .toc import content_file, create_pub_index, write_content_csv


def create_pubs():
    def create_pub(name, doc_path):
        return update_record(name, doc_path)

    def pub_locations():
        return dict(
            #
            # Books
            journey="Documents/seamansguide.com/journey",
            poem="Documents/seamansguide.com/poem",
            quest="Documents/seamansguide.com/quest",
            leverage="Documents/seamansguide.com/leverage",
            webapps="Documents/seamansguide.com/webapps",
            #
            # Blogs
            tech="Documents/shrinking-world.com/blog",
            write="Documents/seamanslog.com/write",
            sampler="Documents/seamanslog.com/sampler",
            spiritual="Documents/spiritual-things.org/daily",
            mark="Documents/markseaman.org",
            family="Documents/seamanfamily.org",
            today="Documents/markseaman.org/today",
            #
            # Slides
            org="Documents/shrinking-world.org",
            #
            # Video
            # video="Documents/seamanslog.com/video",
            #
            # Private
            private="Documents/markseaman.info",
            io="Documents/shrinking-world.io/ghost.org",
            ai="Documents/shrinking-world.com/ai",
            genetics="Documents/Shrinking-World-Pubs/Genetics/Book",
            sweng="Documents/Shrinking-World-Pubs/SoftwareEngineering/Book",
            #
            # Extra
            # training="Documents/shrinking-world.com/blog/training",
            # projects="Documents/shrinking-world.com/blog/projects",
        )

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
        b.auto_index = s.get("auto_index", False)
        b.auto_contents = s.get("auto_contents", False)
        b.index_folders = s.get("index_folders", False)
        b.index_months = s.get("index_months", False)
        b.save()
        return b

    log = "Create pubs:\n\n"
    pubs = pub_locations()
    for pub in pubs:
        pub = create_pub(pub, pubs[pub])
        log += f"{pub}\n"
    return log


def import_pub(pub):
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
        content = read_csv_file(index)
        for row in content:
            if row[2:]:
                set_content(pub, "chapter", row[0], row[1], row[2])
            elif row:
                set_content(pub, "folder", row[0], 0, row[1])

    def delete_extra_objects(pub):
        Content.objects.filter(blog=pub, retain_object=False).delete()
        for c in Content.objects.filter(blog=pub):
            c.retain_object = False
            c.save()

    content = content_file(pub)
    if pub.auto_contents:
        # print("CREATE CONTENT")
        write_content_csv(pub)
    import_content(pub, content)
    delete_extra_objects(pub)


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
