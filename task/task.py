from datetime import datetime, timedelta
from os import system
from pathlib import Path
from re import findall, sub
from django.db.models import Sum
from django.template.loader import render_to_string
from os.path import exists, join

from publish.days import recent_dates
from publish.text import text_join, text_lines
from task.models import Activity, Task, TaskType


def task_dates(days=7):
    # def task_text_list(tasks):
    #     def format(t):
    #         return "%s %s\n\n%s\n" % (
    #             t.name,
    #             t.hours,
    #             t.notes.strip("\n").replace("      ", "  "),
    #         )

    #     return "\n".join([format(t) for t in tasks])

    # def daily_report(t):
    #     date = t.strftime("%Y-%m-%d")
    #     summary = task_text_list(Task.objects.filter(date=t))
    #     return date, summary

    tasks = Task.objects.all()
    if days != "all":
        tasks = time_filter(Task.objects.all(), days)

    dates = tasks.order_by("date").values("date").distinct()
    dates = [t["date"].strftime("%Y/%m/%d") for t in dates]
    return dates
    # return [daily_report(t) for t in dates]


# def bad_days():
#     end = datetime.now()
#     start = end - timedelta(days=365)
#     tasks = Task.objects.filter(date__gt=start, date__lte=end)
#     totals = tasks.values("date").annotate(
#         task_hours=Sum("hours")).order_by("-date")
#     return [(str(t["date"]), t["task_hours"]) for t in totals if t["task_hours"] != 14]

def missing_days(days):
    for d in recent_dates(days):
        if not Task.objects.filter(date=d):
            print(f'Missing {d}')
    return 'x'


def bad_days_data(days):
    end = datetime.now()
    start = end - timedelta(days=days)
    tasks = Task.objects.filter(date__gt=start, date__lte=end)
    totals = tasks.values("date").annotate(
        task_hours=Sum("hours")).order_by("-date")
    table = [(str(t["date"]), t["task_hours"])
             for t in totals if t["task_hours"] != 14]
    return table


def combine_work_tasks(table, total):
    work = 0
    results = []
    for row in table:
        if row[0] in work_types():
            work += row[1]
        else:
            results.append(row)
    if total != 0:
        results = [("Work", work, "%4.0f" % (work * 100 / total))] + results
        return results


def fix_tasks():
    def find_tasks(text):
        return findall(r'\n[A-Z][a-z]* *\d*', text)

    def replace_task(t1, t2, text):
        return sub(rf'\n{t1} *(\d*)', fr'\n{t2} \1', text)

    def task_in_files(task):
        directory = Path("Documents/markseaman.info/history")
        for path in directory.rglob("*/*"):
            if path.is_file():
                text = path.read_text()
                tasks = findall(rf'\n{task} *\d*', text)
                if tasks:
                    print(path, tasks)

    def rename_task(old_task, new_task):
        directory = Path("Documents/markseaman.info/history")
        for path in directory.rglob("*/??"):
            if path.is_file():
                # print(path)
                text = path.read_text()
                text = replace_task(old_task, new_task, text)
                path.write_text(text)

    def show_activities():
        for a in Activity.objects.all():
            print(a.type.name, a.name)

    def define_activity(name, type):
        type = TaskType.objects.get_or_create(name=type)[0]
        return Activity.objects.get_or_create(name=name, type=type)[0]

    def setup_activities():
        define_activity('Family', 'People')
        define_activity('Learn', 'Work')
        define_activity('Software', 'Work')
        define_activity('ProMETA', 'Work')

        # rename_task('Family', 'People')
        rename_task('Tools', 'Code')
        rename_task('Code', 'Software')
        rename_task('Career', 'Business')
        # rename_task('Networking', 'Business')

        task_in_files('Career')

    setup_activities()
    show_activities()


def import_tasks():
    task_import_files(31)
    # print(time_table("Month", 31))


def monthly_tasks(month):
    def group_tasks(tasks, name):
        groups = unique_activities(tasks, name)
        return [dict(name=g, notes=gather_notes(tasks.filter(name=g))) for g in groups]

    def unique_activities(records, field):
        return [a[0] for a in records.order_by(field).values_list(field).distinct()]

    def gather_notes(group):
        notes = set()
        for t in group:
            for x in text_lines(t.notes):
                notes.add(x)
        return notes

    tasks = Task.objects.filter(date__month=month).order_by("name")
    return group_tasks(tasks, "name")


def percent(actual, total):
    if total == 0:
        return 0
    else:
        return round((float(actual) * 100) / total)


def percent_display(amount, total):
    return "%4.0f" % percent(amount, total)


def percent_totals(totals, subtotals):
    return [
        [task[0]]
        + [percent_display(hours, subtotals[i])
           for i, hours in enumerate(task[1:])]
        for task in totals
    ]


def print_task_history(args):
    def print_tasks(tasks):
        for t in tasks:
            print("%s\n" % t.date)
            print("    %s %s" % (t.name, t.hours))
            if t.notes:
                print(t.notes + "\n")

    def task_select(task_type=None, days=None):
        if days:
            end = datetime.now()
            start = end - timedelta(days)
            tasks = Task.objects.filter(date__gt=start, date__lte=end)
        else:
            tasks = Task.objects.all()
        if task_type:
            tasks = tasks.filter(name=task_type)
        return tasks

    if args:
        task = args[0]
        print("# %s Task History\n\n" % task)
    else:
        task = None
        print("# History for All Tasks\n\n")

    tasks = task_select(task, None)
    print_tasks(tasks)
    return tasks


def save_data():
    system("python manage.py dumpdata --indent 4 task > config/task.json")


def show_task_summary(**kwargs):
    def gather_totals(pairs):
        s = {}
        for i in pairs:
            s.setdefault(i[0], []).append(i[1])
        return s

    def percent(items):
        x = 0
        for i in items:
            x += int(i[2].strip())
        return x

    def show_totals(summary):
        output = ''
        for i in summary:
            output += f'{i:10} {percent(summary[i])}%\n'
            for j in summary[i]:
                info = f'    {j[0]:15} {j[1]:4} hr {j[2]}%'
                output += f'{info}\n'
        return output

    def task_summary(table):
        summary = []
        for t in table:
            a = Activity.objects.filter(name=t[0].strip())
            if a:
                group = a[0].type.name
                activity = a[0].name
                summary.append((group, (activity, t[1], t[2])))
            else:
                print('\n*********** No Activity', t[0].strip())
                assert (False)
        return summary

    days = kwargs.get('days', 366)
    totals = time_totals(days)
    table, total = time_percentage(totals)
    summary = task_summary(table)
    output = show_totals(gather_totals(summary))
    return f"{output}\n\nTotal Hours: {total}"


def tabs_data(tables):
    def options(i, tab, selected):
        data = tab
        if selected:
            data.update(
                dict(name=f"tab{i}", active="active",
                     show="show", selected="true")
            )
        else:
            data.update(
                dict(name=f"tab{i}", active="", show="", selected="false"))
        return data

    def set_options(tabs):
        return [options(i, tab, i == 0) for i, tab in enumerate(tabs)]

    return set_options(tables)


def task_filter(tasks, activity):
    if activity == "Work":
        return tasks.filter(name__in=work_types())


def task_import_files(days=7):
    def read_task_file(date):
        # print(date)
        history = "Documents/markseaman.info/history"
        path = join(history, date.replace("-", "/"))
        if exists(path):
            text = open(path).read()
            # print(path)
            tasks = []
            notes = []

            for line in text.split("\n"):
                if line and not line.startswith(" "):
                    if notes:
                        t = new_task(date, activity, hours, notes)
                        tasks.append("%s -- %s hours" % (t.name, t.hours))
                    words = line.split(" ")
                    activity = words[0]
                    if words[1:]:
                        hours = words[1]
                    else:
                        hours = 0
                    notes = []
                elif line:
                    notes.append(line)
                # print(line)
            if notes:
                # print(date, activity, hours, notes)
                t = new_task(date, activity, hours, notes)
                tasks.append("%s -- %s hours" % (t.name, t.hours))

    def new_task(date, name, hours, notes):
        t = Task.objects.get_or_create(date=date, name=name)[0]
        t.hours = hours
        t.notes = "\n".join(notes)
        t.save()
        return t

    for d in recent_dates(days):
        read_task_file(d)
    save_data()


def task_list(days=7):
    def task_text_list(tasks):
        def format(t):
            return "%s %s\n\n%s\n" % (
                t.name,
                t.hours,
                t.notes.strip("\n").replace("      ", "  "),
            )

        return "\n".join([format(t) for t in tasks])

    def daily_report(t):
        date = t.strftime("%Y-%m-%d")
        summary = task_text_list(Task.objects.filter(date=t))
        return date, summary

    tasks = Task.objects.all()
    if days != "all":
        tasks = time_filter(Task.objects.all(), days)

    dates = tasks.order_by("date").values("date").distinct()
    dates = [t["date"] for t in dates]
    return [daily_report(t) for t in dates]


def time_data():
    tables = [time_table("week", 8), time_table(
        "month", 31), time_table("year", 366)]
    return dict(tabs=tabs_data(tables), incomplete=bad_days_data(366))


def time_filter(tasks, days):
    end = datetime.now()
    start = end - timedelta(days=days)
    # print('time filter', start, end)
    return tasks.filter(date__gt=start, date__lte=end)


def time_summary():
    return render_to_string('time_summary.md', time_table("week", 8))


def time_percentage(totals):
    total = sum([t["task_hours"] for t in totals])
    table = [
        (f'{t["name"]:10}', t["task_hours"],
         percent_display(t["task_hours"], total))
        for t in totals
    ]
    return table, total


def time_totals(days):
    tasks = time_filter(Task.objects.all(), days)
    totals = (
        tasks.values("name").annotate(
            task_hours=Sum("hours")).order_by("-task_hours")
    )
    return totals


def time_table(period, days):
    totals = time_totals(days)
    table, total = time_percentage(totals)
    labels = ["Task Name", "Invested Time", "Percentage"]
    description = f"Total hours spent for the previous {period}."
    data = {
        "tab": period,
        "period": period,
        "description": description,
        "total": total,
        "labels": labels,
        "table": table,
    }
    return data


def work_types():
    return "Hire,Aspire,Business,Family,Pantograph,Teach,Tools,WAM,Sign,Write,Hammer".split(
        ","
    )
