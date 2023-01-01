from os import listdir
from os.path import exists

from django.template.loader import render_to_string

from course.course import get_course
from course.models import Content
from publish.image import fix_images
from publish.files import read_file, read_json, write_file
from publish.text import text_join, text_lines


def build_slides(markdown_path, website_path, course):
    def build_slide_deck(slides_file, markdown_file, **kwargs):
        text = read_file(markdown_file)
        text = render_slides(text, **kwargs)
        template_name = "course_slides.html"
        kwargs["text"] = text
        html = render_to_string(template_name, kwargs)
        write_file(slides_file, html)

    markdown = f"{markdown_path}/lesson"
    assert exists(markdown)

    slides = f"{website_path}/slides"
    assert exists(slides)

    json = f"Documents/shrinking-world.com/{course}/slides_settings.json"
    assert exists(json)
    settings = read_json(json)
    assert settings

    for s in listdir(markdown):
        lesson = s.replace(".md", "")
        settings["lesson"] = lesson
        markdown_file = f"{markdown}/{s}"
        slides_file = f"{slides}/{lesson}.html"
        build_slide_deck(slides_file, markdown_file, **settings)


def render_slides(text, **kwargs):
    def slides_text(text):
        slides = ["### " + s for s in text.split("### ")[1:]]
        return slides

    def create_slide_section(title, body):
        return dict(title=title, text=body, slides=slides_text(body))

    def render_sections(markdown_text, **kwargs):
        output = []
        sections = markdown_text.split("\n## ")
        for text in sections:
            image_path = kwargs.get("images")
            body = fix_images(text, image_path)
            title = text_lines(text)[0]
            settings = create_slide_section(title, body)
            output.append(settings)
        return output

    def render_section(section, kwargs):
        kwargs.update(section)
        return render_to_string("slides_section.html", kwargs)

    return text_join(
        [render_section(s, kwargs) for s in render_sections(text, **kwargs)][1:]
    )


def slides_view_context(**kwargs):
    course = get_course(kwargs["course"])
    lesson = Content.objects.get(course=course, order=kwargs["order"], doctype="lesson")
    json = f"Documents/shrinking-world.com/{course.name}/slides_settings.json"
    kwargs = read_json(json)
    course = kwargs["course"]
    title = f"{course} - Lesson {lesson.order}"
    # md_path = f'Documents/shrinking-world.com/{course.name}/lesson/{lesson.order:02}.md'
    md_text = read_file(lesson.document)
    text = render_slides(md_text, **kwargs)
    kwargs.update(dict(server=True, title=title, text=text))
    return kwargs
