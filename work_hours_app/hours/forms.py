from django import forms
from .models import WorkEntry, HourlyRate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class WorkEntryForm(forms.ModelForm):
    class Meta:
        model = WorkEntry
        fields = ['date', 'start_time', 'end_time', 'hours_worked', 'hourly_rate', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
class HourlyRateForm(forms.ModelForm):
    class Meta:
        model = HourlyRate
        fields = ['rate', 'effective_from']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Wymagane. Podaj poprawny adres email.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
