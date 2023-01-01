from django.db import models
from django.utils.timezone import now


class Task (models.Model):
    name     = models.CharField(max_length=100)
    notes    = models.TextField(null=True, blank=True)
    date     = models.DateField(default=now)
    hours    = models.IntegerField(default=0)
    done     = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name + ', ' + str(self.date)

    def as_row(self):
        return [self.pk, self.name, self.date, self.hours, self.notes.split('\n') if self.notes else None]

    @staticmethod
    def labels():
        return ['ID', 'Activity', 'Date', 'Hours', 'Details']
