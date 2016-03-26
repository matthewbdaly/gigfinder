from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from gigs.forms import LookupForm
from gigs.models import Event
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.template import RequestContext

class LookupView(FormView):
    form_class = LookupForm

    def get(self, request):
        return render_to_response('gigs/lookup.html', RequestContext(request))

    def form_valid(self, form):
        # Get data
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']

        # Get next week's date
        next_week = timezone.now() + timezone.timedelta(weeks=1)

        # Get Point
        location = Point(latitude, longitude, srid=4326)

        # Look up events
        events = Event.objects.filter(datetime__lte=next_week).annotate(distance=Distance('venue__location', location)).order_by('distance')[0:2]

        # Render the template
        return render_to_response('gigs/lookupresults.html', {
            'events': events
            })
