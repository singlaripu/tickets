from rest_framework import serializers

from .models import Post




class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
        			'id',
        			'author',
        			'city', 
        			'category', 
        			'event', 
        			'venue', 
        			'showtime',
        			'created_on',
        			'fb_link',
        			'mobile'
        		)
        read_only_fields = ('id', 'created_on')
