from django.conf.urls import url
from gigs.views import LookupView

urlpatterns = [
    # Lookup
    url(r'', LookupView.as_view(), name='lookup'),
]
