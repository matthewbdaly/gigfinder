from django.contrib.gis.db import models

class Venue(models.Model):
    """
    Model for a venue
    """
    name = models.CharField(max_length=200)
    location = models.PointField()

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Model for an event
    """
    name = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    venue = models.ForeignKey(Venue)

    def __str__(self):
        return "%s - %s" % (self.name, self.venue.name)
