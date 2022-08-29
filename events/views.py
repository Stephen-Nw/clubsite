from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from datetime import datetime
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
import csv


# MODULES FOR PDF IMPORT
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# IMPORT PAGINATION MODULES
from django.core.paginator import Paginator


# Search for events on events page
def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(description__contains=searched)
        return render(request, 'events/search_events.html', {'searched': searched, 'events': events})
    else:
        return render(request, 'events/search_events.html', {})


# create filtered event list for logged in user
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, 'events/my_events.html', {"events": events})
    else:
        messages.success(request, ("You are not authorized to view this page"))
        return redirect('home')


# Generate PDF venue list
def venue_pdf(request):
    # Create Bytestream buffer
    buffer = io.BytesIO()
    # Create a canvas
    cvs = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    # Create a text object
    textobj = cvs.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont("Helvetica", 14)

    # Designate The Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")

    # Loop
    for line in lines:
        textobj.textLine(line)

    # Finish up
    cvs.drawText(textobj)
    cvs.showPage()
    cvs.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='venue.pdf')


# Generate csv file venue list
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate The Model
    venues = Venue.objects.all()

    # Add column headings to the csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code',
                    'Phone Number', 'Web Address', 'Email'])

    #  Loop through and output to list
    for venue in venues:
        writer.writerow([
            venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])

    return response


# Generate text file venue list
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # Designate The Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    #  Loop through and output to list
    for venue in venues:
        lines.append(
            f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n')

    # lines = ['This is line 1\n',
    #          'This is line 2\n',
    #          'This is line 3\n\n'
    #          'This is cool\n']

    # Write to TextFile
    response.writelines(lines)
    return response


# Delete a venue
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')


# Delete an event
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted"))
        return redirect('list-events')
    else:
        messages.success(
            request, ("You are not authorized to delete this event!!"))
        return redirect('list-events')


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html', {'event': event, 'form': form})


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user  # logged in user
                event.save()
                # form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # Just going to page, not
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None,
                     request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html', {'venue': venue, 'form': form})


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venues})
    else:
        return render(request, 'events/search_venues.html', {})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html', {'venue': venue, 'venue_owner': venue_owner})


def list_venues(request):
    # venue_list = Venue.objects.all().order_by('name')

    # Set up Pagination
    paginate = Paginator(Venue.objects.all(), 3)
    page = request.GET.get('page')
    venues = paginate.get_page(page)
    nums = 'a' * venues.paginator.num_pages

    return render(request, 'events/venue.html', {'venues': venues, 'nums': nums})
    # return render(request, 'events/venue.html', {"venue_list": venue_list, 'venues': venues})


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            venue = form.save(commit=False)
            venue.owner = request.user.id  # logged in user
            venue.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


def all_events(request):
    event_list = Event.objects.all().order_by('name', 'venue')
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

    # Query the Events Model for Dates
    event_list = Event.objects.filter(
        event_date__year=year,
        event_date__month=month_number
    )

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
        "event_list": event_list,
    })
