from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Tickets.views.home', name='home'),
    url(r'^', include('listings.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
