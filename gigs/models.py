from django.contrib.gis.db import models

class Venue(models.Model):
    """
    Model for a venue
    """
    name = models.CharField(max_length=200)
    location = models.PointField()
