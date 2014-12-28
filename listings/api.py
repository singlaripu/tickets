from rest_framework import serializers, status
from .models import Post

from django.http import Http404, HttpResponse

from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils import timezone
from .serializers import PostSerializer

import os, sys, pymongo, urllib, json, pytz
from datetime import datetime, date, time

from .utility import *
import tasks

# MongoDB connection init
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
    """
    Get list of cities
    """
    collection = mongodb['regions']

    now, naive_cutoff_time = get_naive_cutoff_time()
    id = 'regions'

    try:
        result = collection.find({'id': id}).next()
        data = result['data']

        if now > naive_cutoff_time and result['timestamp'] < naive_cutoff_time:
            result = {}
            old_timestamp = True

    except StopIteration:
        result = {}
        old_timestamp = False

    if not result:
        url = 'http://in.bookmyshow.com/getJSData/?cmd=GETREGIONS&1102'
        textvalue = urllib.urlopen(url).readlines()[0]
        jsonvalue = '{%s}' % (textvalue.split('{', 1)[1].rsplit('};var', 1)[0],)
        dump = json.loads(jsonvalue)
        data = [city for key, value in dump.iteritems() for city in value]

        if old_timestamp:
            collection.update(
                    {'id': id},
                    {
                        '$set' : {
                            'data' : data,
                            'timestamp' : now
                        }
                    }
                )
        else:
            collection.insert({
                    'id' :  id,
                    'data' : data,
                    'timestamp' : now
                })

    return HttpResponse(json.dumps(data), content_type="application/json")



def get_movies(request, city):
    """
    Get a list of movies in a city
    # sample image links: 
    # http://cnt.in.bookmyshow.com/Events/large/ET00025297.jpg
    # http://cnt.in.bookmyshow.com/Events/Mobile/ET00027059.jpg
    """

    collection = mongodb['movies']
    
    now, naive_cutoff_time = get_naive_cutoff_time()
    id = city

    try:
        result = collection.find({'id':id}).next()
        data = result['data']

        if now > naive_cutoff_time and result['timestamp'] < naive_cutoff_time:
            result = {}
            old_timestamp = True

    except StopIteration:
        result = {}
        old_timestamp = False

    if not result:
        url = 'http://in.bookmyshow.com/getJSData/?file=/data/js/GetEvents_MT.js&cmd=GETEVENTSWEB&et=MT&rc=' + city
        textvalue = urllib.urlopen(url).readlines()[0]
        jsonvalue = '{"movies":%s}' % (textvalue.split('aiEV=', 1)[1].rsplit(';aiSRE=', 1)[0],)
        dump = json.loads(jsonvalue)
        data = [{'code':i[1], 'name':i[4], 'url': i[10] } for i in dump['movies'] ]

        if old_timestamp:
            collection.update(
                    {'id' : id},
                    {
                        '$set' : {
                            'data' : data,
                            'timestamp' : now
                        }
                    }
                )
        else:
            collection.insert({
                    'id' : id,
                    'data' : data,
                    'timestamp' : now
                })

        tasks.upload.delay([i['code'] for i in data])

    return HttpResponse(json.dumps(data), content_type="application/json")



def get_events(request, city, category):
    """
    Get a list of events in a city
    categories = CT : Events, SP - Sports, PL - Plays, PT - Parties
    """
    mapping = {
        'CT' : 'events',
        'SP' : 'sports',
        'PL' : 'plays',
        'PT' : 'parties'
    }

    collection = mongodb[mapping[category]]

    now, naive_cutoff_time = get_naive_cutoff_time()
    id = city

    try:
        result = collection.find({'id':id}).next()
        data = result['data']

        if now > naive_cutoff_time and result['timestamp'] < naive_cutoff_time:
            result = {}
            old_timestamp = True

    except StopIteration:
        result = {}
        old_timestamp = False

    if not result:
        url = 'http://in.bookmyshow.com/getJSData/?cmd=GETEVENTLIST&f=json&et=' + \
                category + '&rc=' + city + '&pt=WEB&sr=&lt=&lg='

        jsonvalue = urllib.urlopen(url).readlines()[0]
        dump = json.loads(jsonvalue)

        data = []

        for i in dump['BookMyShow']['arrEvent']:
            if i['arrVenues'][0]['RegionCode'] == city:
                d = {}
                d['code'] = i['EventCode']
                d['name'] = i['EventTitle']
                # d['img'] = i['BannerURL']
                d['url'] = i['FShareURL']
                d['date'] = i['EventReleaseDate']
                d['venue'] = []

                for j in i['arrVenues']:
                    if j['RegionCode'] == city:
                        d1 = {}
                        d1['name'] = j['VenueName']
                        d1['code'] = j['VenueCode']
                        d['venue'].append(d1)

                data.append(d)

        if old_timestamp:
            collection.update(
                    {'id':id},
                    {
                        '$set' : {
                            'data' : data,
                            'timestamp' : now
                        }
                    }
                )
        else:
            collection.insert({
                    'id' : id,
                    'data' : data,
                    'timestamp' : now
                })

        tasks.upload.delay([i['code'] for i in data])

    return HttpResponse(json.dumps(data), content_type="application/json")



def get_cinemas(request, city):
    """
    Get a list of cinemas in a city
    """
    collection = mongodb['cinemas']

    now, naive_cutoff_time = get_naive_cutoff_time()
    id = city

    try:
        result = collection.find({'id':id}).next()
        data = result['data']

        if now > naive_cutoff_time and result['timestamp'] < naive_cutoff_time:
            result = {}
            old_timestamp = True

    except StopIteration:
        result = {}
        old_timestamp = False

    if not result:
        url = 'http://in.bookmyshow.com/getJSData/?file=/data/js/GetVenues_MT_' + \
                city + '.js&cmd=GETVENUESWEB&et=MT&rc=' + city

        textvalue = urllib.urlopen(url).readlines()[0]
        jsonvalue = '{"cinemas":%s]}' % (textvalue.split('aiVN=', 1)[1].rsplit('];', 1)[0],)
        dump = json.loads(jsonvalue)
        data = [{'code':i[0], 'name':i[2]} for i in dump['cinemas']]

        if old_timestamp:
            collection.update(
                    {'id':id},
                    {
                        '$set' : {
                            'data' : data,
                            'timestamp' : now
                        }
                    }
                )
        else:
            collection.insert({
                    'id' : id,
                    'data' : data,
                    'timestamp' : now
                })

    return HttpResponse(json.dumps(data), content_type="application/json")


