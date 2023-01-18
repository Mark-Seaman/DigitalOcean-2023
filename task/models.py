from django.db import models
from django.utils.timezone import now


class TaskType(models.Model):
    name = models.CharField(max_length=100)


class Activity(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(TaskType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type.name}: {self.name}'


class Task (models.Model):
    name = models.CharField(max_length=100)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    notes = models.TextField(null=True, blank=True)
    date = models.DateField(default=now)
    hours = models.IntegerField(default=0)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ', ' + str(self.date)

    def as_row(self):
        return [self.pk, self.name, self.date, self.hours, self.notes.split('\n') if self.notes else None]

    @staticmethod
    def labels():
        return ['ID', 'Activity', 'Date', 'Hours', 'Details']
