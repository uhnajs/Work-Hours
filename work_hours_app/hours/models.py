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
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    hourly_rate = models.ForeignKey(HourlyRate, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
