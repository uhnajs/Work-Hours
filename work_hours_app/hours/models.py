# hours/models.py

from django.db import models
from django.contrib.auth.models import User

class HourlyRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    effective_from = models.DateField()

    def __str__(self):
        return f"{self.rate} PLN/h od {self.effective_from}"

class WorkEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)  # Pole numeryczne
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            delta = datetime.combine(date.min, self.end_time) - datetime.combine(date.min, self.start_time)
            self.hours_worked = delta.total_seconds() / 3600
        super(WorkEntry, self).save(*args, **kwargs)