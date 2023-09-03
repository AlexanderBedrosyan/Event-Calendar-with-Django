from django import forms
from django.forms import ModelForm
from .models import Venue, Event

# Create a venue form


class VenueForm(ModelForm):
    class Meta: # this is not a python convention, it's a Django convention about the idea of ModelForm
        model = Venue
        # fields = "__all__" # with this, we are going to create a form for all of the fields in class Venue from models
        fields = ("name", "address", "zip_code", "phone", "web", "email_address") # this is the way to create only part of the columns that you need
        labels = {
            "name": '', # we are changing the text over the boxes
            "address": '',
            "zip_code": '',
            "phone": '',
            "web": '',
            "email_address": '',
        }
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Venue Name'}), # convention of the way of fix the looks on the page, 'form-control' is coming from getbootstrap
            "address": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Address'}),
            "zip_code": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Zip Code'}),
            "phone": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Phone'}),
            "web": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Web Address'}),
            "email_address": forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email'}),
        }


# superuser form
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ["name", "event_date", "venue", "manager", "attendees", "description"]
        labels = {
            "name": '',
            "event_date": 'YYYY-MM-DD HH:MM:SS',
            "venue": 'Venue', # for the key when we fill the "Venue" this would be use in the page as name over the box
            "manager": 'Manager',
            "attendees": 'Attendees',
            "description": '',
        }
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Event Name'}),
            "event_date": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Event Date'}),
            "venue": forms.Select(attrs={'class': 'form-select', 'placeholder':'Venue'}), # class: from-select change the view of the button to looks like one for selecting
            "manager": forms.Select(attrs={'class': 'form-select', 'placeholder':'Manager'}), # Command Select give us a chance to select from already created managers
            "attendees": forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder':'Attendees'}), # SelectMultiple give us a chance to select more than one
            "description": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}), # command Textarea makes a big text area
        }


# regular user form
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["name", "event_date", "venue", "attendees", "description"]
        labels = {
            "name": '',
            "event_date": 'YYYY-MM-DD HH:MM:SS',
            "venue": 'Venue', # for the key when we fill the "Venue" this would be use in the page as name over the box
            "attendees": 'Attendees',
            "description": '',
        }
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Event Name'}),
            "event_date": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Event Date'}),
            "venue": forms.Select(attrs={'class': 'form-select', 'placeholder':'Venue'}), # class: from-select change the view of the button to looks like one for selecting
            "attendees": forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder':'Attendees'}), # SelectMultiple give us a chance to select more than one
            "description": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}), # command Textarea makes a big text area
        }
