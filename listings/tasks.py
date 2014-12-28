from __future__ import absolute_import
import pymongo
import cloudinary
import cloudinary.uploader
import cloudinary.api
from celery import shared_task
import os


# MongoDB connection init
client = pymongo.MongoClient(os.environ['MONGOLAB_URI'])
mongodb = client.get_default_database()


# Cloudinary connection init
# Uploaded image url- https://res.cloudinary.com/hscc9cmcb/image/upload/ET00014979.jpg
cloudinary_url = os.environ['CLOUDINARY_URL']
cloud_name = cloudinary_url.rsplit('@',1)[1]
api_key = cloudinary_url.split('://',1)[1].split(':',1)[0]
api_secret = cloudinary_url.rsplit(':',1)[1].split('@',1)[0]

cloudinary.config( 
  cloud_name = cloud_name, 
  api_key = api_key, 
  api_secret = api_secret
)


@shared_task
def upload(l):
    collection = mongodb['images']
    for id in l:
        try:
            result = collection.find({'id':id}).next()
        except StopIteration:
            url = 'http://cnt.in.bookmyshow.com/Events/Large/' + id + '.jpg'
            cloudinary.uploader.upload(url, public_id=id)
            collection.insert({
                    'id' :  id,
                    'data' : True,
                })










