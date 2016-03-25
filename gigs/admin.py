from django.contrib import admin
from gigs.models import Venue, Event
from django.forms import ModelForm
from floppyforms.gis import PointWidget, BaseGMapWidget

class CustomPointWidget(PointWidget, BaseGMapWidget):
    class Media:
        js = ('/static/floppyforms/js/MapWidget.js',)

class VenueAdminForm(ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'location']
        widgets = {
            'location': CustomPointWidget()
        }

class VenueAdmin(admin.ModelAdmin):
    form = VenueAdminForm

admin.site.register(Venue, VenueAdmin)
admin.site.register(Event)
