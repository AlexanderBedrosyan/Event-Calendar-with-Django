from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from django.contrib.auth.models import User
# Import user model to find the owner
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse
import csv
from django.contrib import messages

# Import Pagination Stuff
from django.core.paginator import Paginator


# Create your views here.

# Show Event
def show_event(request, event_id):
    current_year = datetime_needed().year
    current_month = datetime_needed().month

    event = Event.objects.get(pk=event_id)
    return render(request, 'events/show_event.html', {'event': event,
                                                        'current_year': current_year,
                                                        'current_month': current_month})


# Show Events in a Venue
def venue_events(request, venue_id):
    current_year = datetime_needed().year
    current_month = datetime_needed().month

    # Grab the venue

    venue = Venue.objects.get(id=venue_id)

    # Grab the events

    events = venue.event_set.all()
    if events:
        return render(request, 'events/venue_events.html', {'events': events,
                                                        'current_year': current_year,
                                                        'current_month': current_month})
    else:
        messages.success(request, ("That Venue has no events at this time!"))
        return redirect('admin-approval')


def admin_approval(request):
    current_year = datetime_needed().year
    current_month = datetime_needed().month

    # Get The Venues

    venue_list = Venue.objects.all()

    # Get Count
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == 'POST':
            id_list = request.POST.getlist('boxes')

            # Uncheck all events because it cant be uncheck manually, this is why it should be unchecked first

            event_list.update(approved=False)

            # Update the databese

            for id in id_list:
                Event.objects.filter(pk=int(id)).update(approved=True)

            messages.success(request, ("Event List Approval has been updated!"))
            return redirect('list-events')
        else:
            return render(request, 'events/admin_approval.html', {'event_count': event_count,
                                                                  'venue_count': venue_count,
                                                                  'user_count': user_count,
                                                                  'event_list': event_list,
                                                                  'venue_list': venue_list,
                                                                    'current_year': current_year,
                                                                    'current_month': current_month})

    else:
        messages.success(request, ("You aren't authorized to view this page!"))
        return redirect('home')


def my_events(request):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, 'events/my_events.html', {'events': events,
                                                    'current_year': current_year,
                                                 'current_month': current_month})
    else:
        messages.success(request, ('You cannot see this page!'))
        return redirect('home')


def venue_csv(request):
    response = HttpResponse(content_type='text/csv') # text/csv means that we are going to creat an excell file
    response['Content-Disposition'] = 'attachment; filename=venues.csv' # venues.csv generate excel file
    writer = csv.writer(response)
    venues = Venue.objects.all()
    writer.writerow(['Venue Name', 'Address', 'Phone', 'Zip Code', 'Web Address', 'Email']) # this will write named rows

    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.zip_code, venue.web, venue.email_address])
        # this is the way to fill all rows with the relate text from the Venue Model which is generate in venue = Venue.objects.all()

    return response


def venue_text(request):
    response = HttpResponse(content_type='text/plain') # text/plain, plain means that we are going to generate text file
    response['Content-Disposition'] = 'attachment; filename=venues.txt' # in this row we create the text file
    venues = Venue.objects.all()

    lines = []
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.phone}\n{venue.zip_code}\n{venue.web}\n{venue.email_address}\n\n\n')
    response.writelines(lines)
    return response


def delete_venue(request, venue_id):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')


def delete_event(request, event_id):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ('Event Deleted!'))
        return redirect('list-events')
    else:
        messages.success(request, ("You aren't authorized to delete this event!"))
        return redirect('list-events')


def update_event(request, event_id):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    event = Event.objects.get(pk=event_id) # pk(primary key) which will give us the correct id
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events') #list-venues comes from the url path for venues

    return render(request, 'events/update_event.html', {'event': event,
                                                        'form': form,
                                                 'current_year': current_year,
                                                 'current_month': current_month})


def add_event(request):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
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
                event = form.save()
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # Just Goint To The Page, Not Submmitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm

        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html', {'form': form,
                                                     'submitted': submitted,
                                                    'current_year': current_year,
                                                    'current_month': current_month})


def update_venue(request, venue_id):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    venue = Venue.objects.get(pk=venue_id) # pk(primary key) which will give us the correct id
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues') #list-venues comes from the url path for venues

    return render(request, 'events/update_venue.html', {'venue': venue,
                                                        'form': form,
                                                 'current_year': current_year,
                                                 'current_month': current_month})


def search_venues(request):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    if request.method == "POST":
        searched = request.POST.get('searched', None)
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', {'searched': searched,
                                                             'venues': venues,
                                                 'current_year': current_year,
                                                 'current_month': current_month
                                                 })
    else:
        return render(request, 'events/search_venues.html', {
            'current_year': current_year,
            'current_month': current_month
        })


def search_events(request):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    if request.method == "POST":
        searched = request.POST.get('searched', None)
        events = Event.objects.filter(name__contains=searched)
        return render(request, 'events/search_events.html', {'searched': searched,
                                                             'events': events,
                                                 'current_year': current_year,
                                                 'current_month': current_month
                                                 })
    else:
        return render(request, 'events/search_events.html', {
            'current_year': current_year,
            'current_month': current_month
        })


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id) # pk(primary key) which will give us the correct id
    venue_owner = User.objects.get(pk=venue.owner)
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    return render(request, 'events/show_venue.html', {'venue_owner': venue_owner,
                                                      'venue': venue,
                                                 'current_year': current_year,
                                                 'current_month': current_month})


def list_venues(request):
    # venue_list = Venue.objects.all().order_by('?') # this will order it by random way every time
    venue_list = Venue.objects.all()

    # Set up Pagination
    p = Paginator(Venue.objects.all(), 1) # 2 - means that on every page there have to be only 2 venues, which means that if you have 5 venues, we are going to issue only 3 pages (2/2/1 splitted)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages

    current_year = datetime_needed().year
    current_month = datetime_needed().month
    return render(request, 'events/venue.html', {'venue_list': venue_list,
                                                 'venues': venues,
                                                 'nums': nums,
                                                'current_year': current_year,
                                                'current_month': current_month})


def add_venue(request):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    submitted = False # this means that you have visit the page for the first time and you haven't fill the Venue yet
    if request.method == "POST": #method come from html <form method=POST> and if already press SUBMIT you have to changed submitted to True
        form = VenueForm(request.POST) #if it's posted the details are going to be send to our VenueForm in admin panel
        if form.is_valid(): #part of the details MUST be fill, this is why we have to check if it's valid (details which are not blank=True in models)
            venue = form.save() #if they are valid save it in DB
            venue.owner = request.user.id #this is the way to save the correct id to the owner section
            venue.save()
            return HttpResponseRedirect('/add_venue?submitted=True') #this would be post in to the page
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html', {'form': form,
                                                     'submitted': submitted,
                                                    'current_year': current_year,
                                                    'current_month': current_month})


def datetime_needed():
    now = datetime.now()
    return now


def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    return render(request, 'events/event_list.html', {'event_list': event_list,
                                                      'current_year': current_year,
                                                    'current_month': current_month})


def correct_date(request):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    return render(request, 'events/navbar.html', {'current_year': current_year,
                                                  'current_month': current_month})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Bozhana"
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(year, month_number)

    now = datetime.now()
    current_year = now.year
    # Query The Events Model For Dates

    event_list = Event.objects.filter(
        event_date__year = year,
        event_date__month = month_number
        )

    time = now.strftime('%I:%M %p')

    return render(request, "events/home.html", {"first_name": name,
                                         "year": year,
                                         "month": month,
                                         "month_number": month_number,
                                         "cal": cal,
                                         "current_year": current_year,
                                         "time": time,
                                         "event_list": event_list,
                                         })