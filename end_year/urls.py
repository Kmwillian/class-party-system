from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('events/', include('events.urls', namespace='events')),
    path('rsvp/', include('rsvp.urls', namespace='rsvp')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('', include('rsvp.urls', namespace='rsvp_home')),
]