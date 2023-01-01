from probe.probe import check_lines_in_webpage
from requests import get


def test_shrinking_world():
    return check_lines_in_webpage("https://shrinking-world.com", 110, 250)


def test_tech():
    return check_lines_in_webpage("https://shrinking-world.com/tech/Index", 110, 150)


def test_training():
    return check_lines_in_webpage(
        "https://shrinking-world.com/training/Index", 150, 160
    )


# def test_projects():
#     return check_lines_in_webpage('https://shrinking-world.com/projects/Index', 140, 150)


def test_book():
    return check_lines_in_webpage("https://seamansguide.com/book", 300, 350)


def test_blogs():
    return check_lines_in_webpage("https://seamanslog.com/publish/", 250, 270)


def test_seamanslog():
    return check_lines_in_webpage("https://seamanslog.com", 110, 160)


def test_mark():
    return check_lines_in_webpage("https://markseaman.org", 150, 170)


def test_spiritual_things():
    return check_lines_in_webpage("https://spiritual-things.org", 100, 300)


def test_spiritual_things_daily():
    return get("https://spiritual-things.org/spiritual/Index").text
