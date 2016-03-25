from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Gig URLs
    url(r'', include('gigs.urls')),
]
