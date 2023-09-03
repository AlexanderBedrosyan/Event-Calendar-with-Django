from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('events', views.all_events, name="list-events"),
    path('events', views.correct_date, name="navbar_date"),
    path('add_venue', views.add_venue, name="add-venue"), # add_venue - the html., views.add_venue - func in views, name - how we can call it in html
    path('list_venues', views.list_venues, name='list-venues'),
    path('show_venue/<venue_id>', views.show_venue, name='show-venue'),
    path('search_venues', views.search_venues, name='search-venues'),
    path('update_venue/<venue_id>', views.update_venue, name='update-venue'),
    path('add_event', views.add_event, name='add-event'),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),
    path('delete_venue/<venue_id>', views.delete_venue, name='delete-venue'),
    path('venue_text', views.venue_text, name='venue-text'),
    path('venue_csv', views.venue_csv, name='venue-csv'),
    path('my_events', views.my_events, name='my-events'),
    path('search_events', views.search_events, name='search-events'),
    path('admin_approval', views.admin_approval, name='admin-approval'),
    path('venue_events/<venue_id>', views.venue_events, name='venue-events'),
    path('show_event/<event_id>', views.show_event, name='show-event'),
]
