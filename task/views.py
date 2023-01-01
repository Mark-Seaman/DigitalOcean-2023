from calendar import month_name
from django.views.generic import TemplateView

from publish.files import read_file

from .task import monthly_tasks, task_dates, task_import_files, time_data
from .models import Task


class HistoryView(TemplateView):
    template_name = "history.html"

    def get_context_data(self, **kwargs):
        tasks = monthly_tasks("01")
        # kwargs = dict(month="September, 2022", tasks=tasks)
        kwargs = time_data()
        kwargs["days"] = task_dates()
        return kwargs


class MyTime(TemplateView):
    template_name = "task_time.html"

    def get_context_data(self, **kwargs):
        task_import_files(7)
        kwargs = super(MyTime, self).get_context_data(**kwargs)
        kwargs.update(time_data())
        return kwargs


class MonthView(TemplateView):
    template_name = "month.html"

    def get_context_data(self, **kwargs):
        kwargs["tasks"] = monthly_tasks(kwargs.get("month"))
        kwargs["month"] = month_name[kwargs["month"]]
        return kwargs


class DayView(TemplateView):
    template_name = "day.html"

    def get_context_data(self, **kwargs):
        year = kwargs["year"]
        month = kwargs["month"]
        day = kwargs["day"]
        kwargs["tasks"] = read_file(
            f"Documents/markseaman.info/history/{year}/{month:02}/{day:02}"
        )
        return kwargs
