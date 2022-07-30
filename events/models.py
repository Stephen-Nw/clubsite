from django.db import models

# Create your models here.


class Venue(models.Model):
    name = models.CharField(db_column='Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField(db_column='Zip Code', max_length=30)
    phone = models.CharField(db_column='Contact Phone', max_length=30)
    web = models.URLField(db_column='Website Address')
    email_address = models.EmailField(db_column='Email Address')

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(db_column='User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField(db_column='Event Name', max_length=120)
    event_date = models.DateTimeField(db_column='Event Date')
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
