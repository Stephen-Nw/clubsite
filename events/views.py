from django.shortcuts import render
import calendar
from calendar import HTMLCalender

# Create your views here.


def home(request, month, year):
    name = "Stephen"
    return render(request, 'events/home.html', {
        "name": name,
        "month": month,
        "year": year,
    })
