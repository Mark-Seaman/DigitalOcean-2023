from django.urls import path

from .views import DayView, HistoryView, MonthView, MyTime

urlpatterns = [
    path("task/", MyTime.as_view()),
    path("task/<int:month>", MonthView.as_view()),
    path("history/", HistoryView.as_view()),
    path("history/<int:year>/<int:month>/<int:day>", DayView.as_view()),
]
