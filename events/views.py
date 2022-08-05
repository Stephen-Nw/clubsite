from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from django.http import HttpResponseRedirect
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm


def list_venues(request):
    venue_list = Venue.objects.all()
    return render(request, 'events/venue.html', {"venue_list": venue_list})


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


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
