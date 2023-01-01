from os import system
from pathlib import Path

from course.models import Content, Course
from publish.document import document_title
from publish.files import read_file
from publish.text import text_join, text_lines

total_word_count = 0


def textbook_content(course):
    content = Content.objects.filter(course=course, week=course.week)
    content = content.exclude(doctype="video").exclude(doctype="lesson")
    return content.order_by("course", "week", "doctype", "order")


def show_textbook_content():
    course = Course.objects.get(name="bacs350")
    text = f'# Week {course.week}\n\n'
    for content in textbook_content(course):
        text += read_file(content.document)
    lines = text_lines(text)
    headings = text_join([x for x in lines if x.startswith('#')])
    print(headings)

# def get_content(course, w):
#     def get_records(course, model, order, per_week=1):
#         return model.objects.filter(
#             course=course, order__gte=order, order__lt=order + per_week
#         ).order_by("order")

#     def weekly_records(course, model, label, order, per_week=1):
#         return [i for i in get_records(course, model, order, per_week) if i]

#     records = weekly_records(course, Chapter, "Chapter", w)
#     records += weekly_records(course, Skill, "Skill", w * 3 - 2, 3)
#     records += weekly_records(course, Demo, "Demo", w, 1)
#     records += weekly_records(course, Project, "Project", w, 1)
#     records += weekly_records(course, Lesson, "Lesson", w * 2 - 1, 2)
#     return records


# def course_content():
#     course = Course.objects.get(name="bacs350")
#     files = ["Documents/shrinking-world.com/bacs350/chapter/Intro.md"]
#     # print(f'\nWeek {chapter+1}')
#     for i in range(14):
#         content = get_content(course, i + 1)
#         files += [x.document for x in content]
#         # print(f'   {i[0]} {i[1].order} {i[1].document} {i[1].title}')
#     files += ["Documents/shrinking-world.com/bacs350/chapter/About.md"]
#     return files


def generate_textbook():
    def generate_epub(dir):
        markdown_file = "textbook.md"
        epub_file = "textbook.epub"
        print(f"Creating the epub file - {dir}/{epub_file}")
        css = "-c textbook.css"
        toc = "--toc --toc-depth=1"
        cover = ""
        pandoc = f"pandoc {markdown_file} {css} {toc} {cover} -o {epub_file}"
        system(f"cd {dir} && {pandoc} && ls -l")

    def generate_markdown(dir):
        def content_file(path):
            if not path.exists():
                print(f"Missing file - {path}")
                return f"Missing file - {path}"

            if "lesson" in str(path):
                return ""

            text = path.read_text() + "\n\n"
            title = document_title(path)

            if (
                title.startswith("Chapter ")
                or title.startswith(" Skill ")
                or title.startswith(" Demo ")
            ):
                tail = f"\n\n![](img/Section.jpg)\n\n"
                text = text + tail

            return text

        markdown_file = dir / "textbook.md"
        print(f"Creating the HTML file - {markdown_file}")
        yaml_file = dir / "textbook.yaml"
        book_markdown = yaml_file.read_text()
        # for x in course_content():
        #     book_markdown += content_file(Path(x))
        print("Lines of text: ", len(text_lines(book_markdown)))
        markdown_file.write_text(book_markdown)
        system(f"cd {dir} && grep '^#' textbook.md > textbook.headings")

    dir = Path("Documents/seamansguide.com/webapps")
    generate_markdown(dir)
    # generate_epub(dir)
