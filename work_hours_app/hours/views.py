from django.shortcuts import render
from .models import WorkEntry
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import WorkEntryForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render
from django.utils.safestring import mark_safe
from .utils import Calendar
from datetime import date
import calendar

@login_required
def calendar_view(request, year=None, month=None):
    if year is None:
        year = date.today().year
    if month is None:
        month = date.today().month

    year = int(year)
    month = int(month)

    # Obliczenie poprzedniego i następnego miesiąca
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1

    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    # Nazwa miesiąca
    month_name = calendar.month_name[month]

    work_entries = WorkEntry.objects.filter(user=request.user, date__year=year, date__month=month)
    cal = Calendar(work_entries).formatmonth(year, month)
    context = {
        'calendar': mark_safe(cal),
        'year': year,
        'month': month,
        'month_name': month_name,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }
    return render(request, 'hours/calendar.html', context)

@login_required
def work_entries_list(request):
    entries = WorkEntry.objects.filter(user=request.user)
    return render(request, 'hours/work_entries_list.html', {'entries': entries})



@login_required
def add_work_entry(request):
    if request.method == 'POST':
        form = WorkEntryForm(request.POST)
        if form.is_valid():
            work_entry = form.save(commit=False)
            work_entry.user = request.user
            work_entry.save()
            return redirect('work_entries_list')
    else:
        form = WorkEntryForm()
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