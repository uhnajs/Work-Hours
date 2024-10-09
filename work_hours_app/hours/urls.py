from django.urls import path
from . import views

urlpatterns = [
    path('', views.work_entries_list, name='work_entries_list'),
    path('add/', views.add_work_entry, name='add_work_entry'),
    path('rates/', views.hourly_rates_list, name='hourly_rates_list'),
    path('rates/add/', views.add_hourly_rate, name='add_hourly_rate'),
    path('report/pdf/', views.generate_pdf_report, name='generate_pdf_report'),
]
