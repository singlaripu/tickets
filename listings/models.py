from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.


class Post(models.Model):
    author = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=10, null=True)
    category = models.CharField(max_length=2, null=True)
    event = models.CharField(max_length=255, null=True)
    venue = models.CharField(max_length=255, null=True)
    showtime = models.DateTimeField('Event Time', null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    fb_link = models.URLField(max_length=200, null=True)
    mobile = models.CharField(max_length=20, null=True)



