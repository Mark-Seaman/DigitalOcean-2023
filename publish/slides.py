
from course.slides import render_slides
from publish.files import read_file, read_json


def slides_view_context(**kwargs):
    json = f"Documents/shrinking-world.com/slides/slides_settings.json"
    md_path = f'Documents/shrinking-world.com/slides/01.md'
    kwargs = read_json(json)
    md_text = read_file(md_path)
    text = render_slides(md_text, **kwargs)
    kwargs.update(dict(server=True, text=text))
    return kwargs
