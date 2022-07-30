from django.db import models

# Create your models here.


class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=30)
    phone = models.CharField('Contact Phone', max_length=30)
    web = models.URLField('Website Address')
    email_address = models.EmailField('Email Address')

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    # venue = models.CharField(max_length=120)
    # Use ForeignKey in many-to-one relationships; do not use in many-to-many relationships
    venue = models.ForeignKey(
        'Venue', on_delete=models.CASCADE, blank=True, null=True)
    manager = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)

    # Fxn below allows name of columns do display on admin page
    def __str__(self):
        return self.name
