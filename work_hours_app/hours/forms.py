# hours/forms.py

from django import forms
from .models import WorkEntry, HourlyRate

class WorkEntryForm(forms.ModelForm):
    class Meta:
        model = WorkEntry
        fields = ['date', 'hours_worked', 'description', 'hourly_rate']

class HourlyRateForm(forms.ModelForm):
    class Meta:
        model = HourlyRate
        fields = ['rate', 'effective_from']
