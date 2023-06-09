from pathlib import Path

from publish.publication import all_books

from .probe import check_files


book = Path("Documents") / "seamansguide.com"


def test_book_journey():
    return check_files(book / "journey", 30, 60)


def test_book_poem():
    return check_files(book / "poem", 70, 90)


def test_book_leverage():
    return check_files(book / "leverage", 39, 46)


def test_book_webapps():
    return check_files(book / "webapps", 130, 140)


def test_book_quest():
    return check_files(book / "quest", 60, 70)
