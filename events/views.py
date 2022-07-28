from django.shortcuts import render

# Create your views here.


def home(request, month, year):
    name = "Stephen"
    return render(request, 'events/home.html', {
        "name": name,
        "month": month,
        "year": year,
    })
