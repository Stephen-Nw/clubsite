from django.contrib import admin
from .models import Event, Venue, MyClubUser

# Register your models here.
# Models ar registered on this page so that they show up in the admin area

admin.site.register(Venue)
admin.site.register(MyClubUser)
admin.site.register(Event)
