from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from .api import PostList, get_regions


post_urls = patterns('',
    url(r'^$', PostList.as_view(), name='post-list')
)

urlpatterns = patterns('',
	url(r'^$', 'listings.views.home', name="home"),
	url(r'^api/regions/$', get_regions, name="regions"),
    url(r'^api', include(post_urls)),
)

urlpatterns = format_suffix_patterns(urlpatterns) 

