from django.forms import Form, FloatField

class LookupForm(Form):
    latitude = FloatField()
    longitude = FloatField()
