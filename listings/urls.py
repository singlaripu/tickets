from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from .api import PostList, get_regions, get_movies, get_cinemas, get_events


post_urls = patterns('',
    url(r'^$', PostList.as_view(), name='post-list')
)

urlpatterns = patterns('',
	url(r'^$', 'listings.views.home', name="home"),
	url(r'^api/regions/$', get_regions, name="regions"),
	url(r'^api/movies/(?P<city>[A-Z]{3,8})/$', get_movies, name="movies"),
	url(r'^api/cinemas/(?P<city>[A-Z]{3,8})/$', get_cinemas, name="cinemas"),
	url(r'^api/events/(?P<city>[A-Z]{3,8})/(?P<category>[A-Z]{2})/$', get_events, name="events"),
    url(r'^api', include(post_urls)),
)

urlpatterns = format_suffix_patterns(urlpatterns) 

