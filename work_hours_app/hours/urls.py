from django.urls import path
from . import views
from .views import CustomLogoutView

urlpatterns = [
    path('', views.calendar_view, name='calendar'),  # Główna strona to teraz kalendarz
    path('add_work_entry/', views.add_work_entry, name='add_work_entry'),
    path('rates/', views.hourly_rates_list, name='hourly_rates_list'),
    path('work-entries/', views.work_entries_list, name='work_entries_list'),
    path('rates/add/', views.add_hourly_rate, name='add_hourly_rate'),
    path('report/pdf/', views.generate_pdf_report, name='generate_pdf_report'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar'),
    path('register/', views.register, name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

]
