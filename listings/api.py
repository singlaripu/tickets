from rest_framework import serializers, status
from .models import Post

from django.http import Http404, HttpResponse

from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils import timezone
from .serializers import PostSerializer

import os, sys, pymongo, urllib, json, pytz
from datetime import datetime



client = pymongo.MongoClient(os.environ['MONGOLAB_URI'])
mongodb = client.get_default_database()

class PostList(APIView):
    """
    List posts matching the query, or create a new listing.
    """
    def get(self, request, format=None):
        return Response(request.data)


    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        posts = Post.objects.filter(
                                        city=request.data['city'],
                                        category=request.data['category'],
                                        venue=request.data['venue'],
                                        event=request.data['event'],
                                        showtime__gte=timezone.now()
                                    )
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)



def get_regions(request):
    regions = mongodb['regions']
    try:
        result = regions.find().next()
        data = result['data']

        now = datetime.utcnow()
        cutoff_time = datetime(now.year, now.month, now.day, 3, 30, 0, 0, tzinfo=pytz.utc)
        naive_cutoff_time = cutoff_time.replace(tzinfo=None)

        if result['timestamp'] < naive_cutoff_time:
            result = {}
            old_timestamp = True

    except StopIteration:
        result = {}
        old_timestamp = False

    if not result:
        url = 'http://in.bookmyshow.com/getJSData/?cmd=GETREGIONS&1102'
        textvalue = urllib.urlopen(url).readlines()[0]
        jsonvalue = '{%s}' % (textvalue.split('{', 1)[1].rsplit('};var', 1)[0],)
        data = json.loads(jsonvalue)

        if old_timestamp:
            regions.update(
                    {'id':'regions'},
                    {
                        '$set' : {
                            'data' : data,
                            'timestamp' : datetime.utcnow()
                        }
                    }
                )
        else:
            regions.insert({
                    'id' : 'regions',
                    'data' : data,
                    'timestamp' : datetime.utcnow()
                })

    return HttpResponse(json.dumps(data), content_type="application/json")


