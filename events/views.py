from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event
from .forms import VenueForm


def add_venue(request):
    form = VenueForm
    return render(request, 'events/add_venue.html', {})


def all_events(request):
    event_list = Event.objects.all()
    return render(request, 'events/event_list.html', {"event_list": event_list})


def home(request, month=datetime.now().strftime('%B'), year=datetime.now().year):
    name = "Stephen"

    # Convert month from name to number
    month_number = list(calendar.month_name).index(month.title())
    month_number = int(month_number)

    # Create a calendar... default calendar starts on Monday (firstweekday=0) so this has to be changed to Sunday (firstweekday=6)
    cal = HTMLCalendar(firstweekday=6).formatmonth(year, month_number)

    # Get current year
    now = datetime.now()
    current_year = now.year

    # Get current time
    time = now.strftime('%I:%M:%S %p')

    return render(request, 'events/home.html', {
        "name": name,
        "month": month,
        "year": year,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
    })
