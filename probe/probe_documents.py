from pathlib import Path

from probe.probe import check_files
from publish.document import doc_text
from publish.publication import get_pub
from publish.text import char_fix_files

docs = Path("Documents")


def test_documents_bacs200():
    return check_files(docs / "shrinking-world.com" / "bacs200", 70, 80)


def test_documents_bacs350():
    return check_files(docs / "shrinking-world.com" / "bacs350", 180, 250)


def test_documents_cs350():
    return check_files(docs / "shrinking-world.com" / "cs350", 210, 250)


def test_documents_info():
    return check_files(docs / "markseaman.info", 2800, 3200)


def test_documents_images():
    return check_files(Path("static") / "images", 650, 700)


def test_documents_embedded_images():
    doc_path = Path(f"Documents/Shrinking-World-Pubs/journey/Pub")
    pub = get_pub('journey')
    image_path = pub.image_path
    return doc_text(doc_path / "JFK.md", image_path) + doc_text(
        doc_path / "MushroomCloud.md", image_path
    )


def test_documents_fix_chars():
    return char_fix_files("Documents")


def test_documents_seamanslog():
    return check_files(docs / "seamanslog.com", 300, 450)


def test_documents_seamansguide():
    return check_files(docs / "seamansguide.com", 50, 52)


def test_documents_spiritual():
    return check_files(docs / "spiritual-things.org", 950, 1300)


def test_documents_shrinking_world():
    return check_files(docs / "shrinking-world.com", 700, 710)


def test_documents_mark():
    return check_files(docs / "markseaman.org", 10, 32)


def test_documents_family():
    return check_files(docs / "seamanfamily.org", 5, 20)
