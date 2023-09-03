from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Contact Phone', max_length=250, blank=True)
    web = models.URLField('Website Address', blank=True) # this URLField tracking web addresses
    email_address = models.EmailField('Email Address', blank=True) # this EmailField tracking email addresses
    owner = models.IntegerField('Venue Owner', blank=False, default=1) # its Integer, because every manager has a ID number which are going to be connected with the Owner of each event
                                            # in this case default=1 will add the first admin which is created

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField("User Email")

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    # name ("Event Name") of event we are working with models in the brackets are length of name
    event_date = models.DateTimeField('Event Date') # we are using models DateTimeField, which will help for date charts
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    # this ForeignKey connected two objects in our case Event cls.attribute venue with Venue(obj)
    #venue = models.CharField("Venue", max_length=120)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL) #on_delete if the manager gone this will put null on the box
    description = models.TextField(blank=True) # this means that we are going to have a blank text box
    attendees = models.ManyToManyField(MyClubUser, blank=True) # this connect a lot of obj
    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.name

    @property
    def days_left(self):
        today = date.today()
        days_till = self.event_date.date() - today
        only_the_left_days = str(days_till).split(" ")[0]
        if int(only_the_left_days) <= 0:
            return "Finished"
        else:
            return only_the_left_days

