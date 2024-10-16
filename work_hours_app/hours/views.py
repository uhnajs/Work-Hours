from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from .models import WorkEntry, HourlyRate
from .forms import WorkEntryForm, HourlyRateForm, SignUpForm
from .utils import Calendar

from datetime import date, datetime
import calendar
from xhtml2pdf import pisa
import json


@login_required
def calendar_view(request, year=None, month=None):
    if year is None:
        year = date.today().year
    if month is None:
        month = date.today().month

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    # Pobranie wpisów pracy
    work_entries = WorkEntry.objects.filter(user=request.user, date__year=year, date__month=month)

    # Tworzenie wydarzeń do FullCalendar
    events = []
    for entry in work_entries:
        events.append({
            'title': f"{entry.hours_worked}h - {entry.hourly_rate} PLN/h",
            'start': entry.date.strftime('%Y-%m-%d'),
            'allDay': True,  # Wydarzenie na cały dzień
        })

    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'events': mark_safe(json.dumps(events)),  # Przekazanie wydarzeń jako JSON do szablonu
    }
    return render(request, 'hours/calendar.html', context)

@login_required
def work_entries_list(request):
    entries = WorkEntry.objects.filter(user=request.user)
    return render(request, 'hours/work_entries_list.html', {'entries': entries})

@login_required
def add_work_entry(request):
    date_param = request.GET.get('date')  # Pobranie daty z URL
    if date_param:
        initial_date = datetime.strptime(date_param, '%Y-%m-%d').date()
    else:
        initial_date = None

    if request.method == 'POST':
        form = WorkEntryForm(request.POST)
        if form.is_valid():
            work_entry = form.save(commit=False)
            work_entry.user = request.user
            work_entry.save()
            return redirect('work_entries_list')  # Przekierowanie po poprawnym zapisaniu wpisu
        else:
            print(form.errors)  # Dodaj to, aby sprawdzić, jakie błędy występują
    else:
        form = WorkEntryForm(initial={'date': initial_date})

    return render(request, 'hours/add_work_entry.html', {'form': form})

@login_required
def hourly_rates_list(request):
    rates = HourlyRate.objects.filter(user=request.user)
    return render(request, 'hours/hourly_rates_list.html', {'rates': rates})

@login_required
def add_hourly_rate(request):
    if request.method == 'POST':
        form = HourlyRateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.save()
            return redirect('hourly_rates_list')
    else:
        form = HourlyRateForm()
    return render(request, 'hours/add_hourly_rate.html', {'form': form})

@login_required
def generate_pdf_report(request):
    entries = WorkEntry.objects.filter(user=request.user)
    template = get_template('hours/report.html')
    html = template.render({'entries': entries})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="raport.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
            return redirect('work_entries_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def logout_view(request):
    logout(request)
    return redirect('login')

