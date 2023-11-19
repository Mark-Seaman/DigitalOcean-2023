from pathlib import Path
from course.import_export import import_all_courses
from course.student import import_students
from course.workspace import workspace_path
from probe.data import save_json_data
from publish.days import is_old
from publish.publication import all_pubs, build_pubs, show_pub_json
from writer.words import measure_pub_words


def test_data_json():
    status = 'Data JSON:\n'

    # Pubs
    build_pubs()
    text = save_json_data('config/publish.json', 'publish')
    status += f'    config/publish.json  {len(text)} characters\n'

    # Courses
    import_all_courses()
    s = workspace_path(course='bacs350', project='_students.csv')
    import_students(s)
    text = save_json_data('config/course.json')
    status += f'    config/course.json  {len(text)} characters\n'

    # Tasks
    text = save_json_data('config/task.json', 'task')
    status += f'    config/task.json    {len(text)} characters\n'

    # Data
    text = save_json_data('config/data.json')
    status += f'    config/data.json    {len(text)} characters\n'

    return status
