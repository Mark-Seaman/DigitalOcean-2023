# from pathlib import Path

# from .models import Chapter, Course, Lesson, Project

# def show_course_content(content):
#     for week in content:
#         print(f'Module {week["week"]}')
#         for session in week["lessons"]:
#             print(f"    {session['title']}")
#             print(f"        {session['notes']}")
#             print(f"        {session['slides']}")
#             print(f"        {session['video']}")
#         for c in week["practice"]:
#             print("  ", c.title)

# def lesson_plans():
#     content = ''
#     for course in Course.objects.all():
#         content += f'\n\n-------------------\n\n{course.name}\n\n'
#         plan = lesson_plan(course)
#         for week in plan:
#             content += f'Week {plan[week]["week"]}\n'
#             for lesson in plan[week]['lessons']:
#                 content += f'    {lesson.title} --  {lesson.url}\n'
#             # content += f'    {plan[week]["chapter"].title} -- {plan[week]["chapter"].url}\n'
#             content += f'    {plan[week]["project"].title} -- {plan[week]["project"].url}\n'
#     return content
#
#
# def lesson_plan(course):
#     return {week: weekly_sessions(course, week) for week in course.weeks}
#
# def weekly_plan(course):
#     return [weekly_sessions(course, week) for week in course.weeks]
#
#
# def weekly_sessions(course, week):
#     project = Project.objects.get(course=course, order=week)
#     chapter = Chapter.objects.filter(course=course, order=week)
#     if chapter:
#         chapter = dict(url=chapter[0].url, title=chapter[0].title[8:])
#     lessons = Lesson.objects.filter(course=course, week=week)
#     return dict(week=week, lessons=lessons, project=project, chapter=chapter)
#
#
# def create_new_lessons():
#     def old_text(lesson):
#         path = Path('Documents') / 'shrinking-world.com/cs350/old-lesson'
#         milestone = int(lesson / 4 + 1)
#         old = lesson + milestone * 2
#         if lesson < 4:
#             old += 1
#         elif lesson > 7:
#             old -= 1
#         print(lesson + 1, old, milestone)
#         f = path / f'{old:02}.md'
#         return f.read_text()
#
#     def write_lesson(lesson):
#         f = path / f'{lesson + 1:02}.md'
#         role = ['Requirements', 'Design', 'Code', 'Test'][lesson % 4]
#         title = f'Milestone #{int(lesson / 4) + 1} - {role}'
#         text = f'# Lesson {lesson + 1} - {title}\n\n---\n\n'
#         text += old_text(lesson)
#         f.write_text(text)
#
#     path = Path('Documents') / 'shrinking-world.com/cs350/lesson'
#     for i in range(28):
#         write_lesson(i)
#     for f in sorted(path.iterdir()):
#         print('===========================')
#         print(f.read_text()[:100])
#
#
# def show_course_content():
#     print(lesson_plans())
#     print('Courses', len(Course.objects.all()))
#     print('Chapters', len(Project.objects.all()))
#     print('Lessons', len(Lesson.objects.all()))
#     assert(len(Course.objects.all()) == 3)
#     assert(len(Project.objects.all()) == 37)
#     assert(len(Lesson.objects.all()) == 119)
