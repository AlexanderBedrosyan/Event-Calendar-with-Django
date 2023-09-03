from django.contrib import admin
from .models import *

# admin.site.register(Venue, VenueAdmin)
admin.site.register(MyClubUser)
# admin.site.register(Event)


@admin.register(Venue) # - instead of this row, we can directly add the VenueAdmin in row 4 admin.site.register(Venue, VenueAdmin) and put it below the current class
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone') # this would display the information of exact needed elements
    ordering = ('name',) # if we put "-" in front of "name" ("-name") this will order it from z-a, now it will be order from a-z
    search_fields = ('name', 'address') # this create a search box which can find elements by name and address


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('name', 'venue', 'event_date', 'description', 'manager', 'attendees', 'approved') # this will change the columns in the Event
    list_display = ('name', 'event_date', 'venue') # this is changing the display after the creation in the main admin panel when you click on Event
    list_filter = ('event_date', 'venue') # this is filters that you can use to select by event_date and venue the events which are already created
    ordering = ('-event_date',)