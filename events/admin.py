from django.contrib import admin
from .models import Event, Venue, MyClubUser
from django.contrib.auth.models import Group


# Models are registered on this page so that they show up in the admin area
# admin.site.register(Venue)
# admin.site.register(MyClubUser)
# admin.site.register(Event)


# admin.site.register(Venue)
admin.site.register(MyClubUser)
# admin.site.register(Event)


# Remove Groups
admin.site.unregister(Group)


# CUSTOMIZE THE MODEL DISPLAY IN ADMIN
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    # Selects column from model to display
    list_display = ('name', 'address', 'phone')
    # Which column should be used to sort; don't forget comma
    ordering = ('name',)
    # Add a search bar as well as search parameters
    search_fields = ('name', 'address')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description',
              'manager', 'approved')  # Customize display fields
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')  # Filter parameters
    ordering = ('-event_date',)  # Sort in reverse
