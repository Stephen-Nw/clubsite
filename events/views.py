from django.shortcuts import render
import calendar
from calendar import HTMLCalendar

# Create your views here.


def home(request, month, year):
    name = "Stephen"
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month.title())
    month_number = int(month_number)
    return render(request, 'events/home.html', {
        "name": name,
        "month": month,
        "year": year,
        "month_number": month_number,
    })
