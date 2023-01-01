from requests import get

from publish.text import text_join, text_lines
from probe.probe import check_lines_in_webpage


def test_web_pages():
    urls = '''https://shrinking-world.com
https://markseaman.org
http://google.com
https://apple.com
https://seamanslog.com/publish/
https://seamanslog.com/book/
https://seamanslog.com/book/journey
https://seamanslog.com/book/journey/Part0
https://seamanslog.com
https://seamanslog.com/sampler/Index
https://seamanslog.com/write/Index
'''

    results = [f'{url} - {get(url)}' for url in text_lines(urls) if url]
    return text_join(results)
