from django.test import TestCase
from gigs.models import Venue, Event
from factory.fuzzy import BaseFuzzyAttribute
from django.contrib.gis.geos import Point
import factory.django, random
from django.utils import timezone
from django.test import RequestFactory
from django.core.urlresolvers import reverse
from gigs.views import LookupView

class FuzzyPoint(BaseFuzzyAttribute):
    def fuzz(self):
        return Point(random.uniform(-180.0, 180.0),
                     random.uniform(-90.0, 90.0))

# Factories for tests
class VenueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Venue
        django_get_or_create = (
            'name',
            'location'
        )
    
    name = 'Wembley Arena'
    location = FuzzyPoint()

class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event
        django_get_or_create = (
            'name',
            'venue',
            'datetime'
        )

    name = 'Queens of the Stone Age'
    datetime = timezone.now()

class VenueTest(TestCase):
    def test_create_venue(self):
        # Create the venue
        venue = VenueFactory()

        # Check we can find it
        all_venues = Venue.objects.all()
        self.assertEqual(len(all_venues), 1)
        only_venue = all_venues[0]
        self.assertEqual(only_venue, venue)

        # Check attributes
        self.assertEqual(only_venue.name, 'Wembley Arena')

        # Check string representation
        self.assertEqual(only_venue.__str__(), 'Wembley Arena')


class EventTest(TestCase):
    def test_create_event(self):
        # Create the venue
        venue = VenueFactory()

        # Create the event
        event = EventFactory(venue=venue)

        # Check we can find it
        all_events = Event.objects.all()
        self.assertEqual(len(all_events), 1)
        only_event = all_events[0]
        self.assertEqual(only_event, event)

        # Check attributes
        self.assertEqual(only_event.name, 'Queens of the Stone Age')
        self.assertEqual(only_event.venue.name, 'Wembley Arena')

        # Check string representation
        self.assertEqual(only_event.__str__(), 'Queens of the Stone Age - Wembley Arena')


class LookupViewTest(TestCase):
    """
    Test lookup view
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get(reverse('lookup'))
        response = LookupView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('gigs/lookup.html')

    def test_post(self):
        # Create venues to return
        v1 = VenueFactory(name='Venue1')
        v2 = VenueFactory(name='Venue2')
        v3 = VenueFactory(name='Venue3')
        v4 = VenueFactory(name='Venue4')
        v5 = VenueFactory(name='Venue5')
        v6 = VenueFactory(name='Venue6')
        v7 = VenueFactory(name='Venue7')
        v8 = VenueFactory(name='Venue8')
        v9 = VenueFactory(name='Venue9')
        v10 = VenueFactory(name='Venue10')

        # Create events to return
        e1 = EventFactory(name='Event1', venue=v1)
        e2 = EventFactory(name='Event2', venue=v2)
        e3 = EventFactory(name='Event3', venue=v3)
        e4 = EventFactory(name='Event4', venue=v4)
        e5 = EventFactory(name='Event5', venue=v5)
        e6 = EventFactory(name='Event6', venue=v6)
        e7 = EventFactory(name='Event7', venue=v7)
        e8 = EventFactory(name='Event8', venue=v8)
        e9 = EventFactory(name='Event9', venue=v9)
        e10 = EventFactory(name='Event10', venue=v10)

        # Set parameters
        lat = 52.3749159
        lon = 1.1067473

        # Put together request
        data = {
            'latitude': lat,
            'longitude': lon
        }
        request = self.factory.post(reverse('lookup'), data)
        response = LookupView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('gigs/lookupresults.html')
