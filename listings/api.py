from rest_framework import serializers, status
from .models import Post

from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils import timezone
from .serializers import PostSerializer

class PostList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        return Response(request.data)


    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        print request.data
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