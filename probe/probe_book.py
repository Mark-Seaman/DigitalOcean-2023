from pathlib import Path

from publish.publication import all_books

from .probe import check_files


book1 = Path("Documents") / "Shrinking-World-Pubs"


def test_book_journey():
    return check_files(book1 / "journey", 110, 160)


def test_book_poem():
    return check_files(book1 / "poem", 70, 120)


def test_book_leverage():
    return check_files(book1 / "leverage", 39, 46)


def test_book_webapps():
    return check_files(book1 / "webapps", 130, 140)


def test_book_quest():
    return check_files(book1 / "quest", 90, 100)
