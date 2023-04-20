from probe.probe import check_lines_in_webpage
from publish.files import read_csv_file
from publish.text import text_join


def test_websites_pages():
    pages = read_csv_file('probe/pages.csv')
    pages = [check_lines_in_webpage(p[0], int(p[1]), int(p[2])) for p in pages]
    return text_join(pages)


# def test_websites_blog_list():
#     page = "https://seamanslog.com/publish/blog"
#     return check_lines_in_webpage(page, 250, 270)


# def test_websites_blogs():
#     page = "https://seamanslog.com/publish"
#     return check_lines_in_webpage(page, 250, 270)


# def test_websites_book():
#     page = "https://seamanslog.com/book"
#     return check_lines_in_webpage(page, 300, 350)


# def test_websites_book_list():
#     page = "https://seamanslog.com/publish/book"
#     return check_lines_in_webpage(page, 250, 270)


# def test_websites_mark():
#     page = "https://markseaman.org"
#     return check_lines_in_webpage(page, 150, 170)


# def test_websites_seamanslog():
#     page = "https://seamanslog.com"
#     return check_lines_in_webpage(page, 110, 160)


# def test_websites_spiritual_things():
#     page = "https://spiritual-things.org"
#     return check_lines_in_webpage(page, 100, 300)


# def test_websites_spiritual_things_daily():
#     page = "https://spiritual-things.org/spiritual/Index"
#     return check_lines_in_webpage(page, 250, 270)


# def test_websites_shrinking_world():
#     page = "https://shrinking-world.com"
#     return check_lines_in_webpage(page,  110, 250)


# def test_websites_tech():
#     page = "https://shrinking-world.com/tech/Index"
#     return check_lines_in_webpage(page, 150, 160)


# def test_websites_training():
#     page = "https://shrinking-world.com/tech/training-Index"
#     return check_lines_in_webpage(page, 2150, 160)
