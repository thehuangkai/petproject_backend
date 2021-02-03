import json
import logging
from rest_framework.parsers import JSONParser 
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status

@api_view(['GET','POST'])
def posts(request):
    
    if request.method == 'GET': 
        posts = Post.objects.filter(status=1).order_by('-created_at')
        posts_serializer = PostSerializer(posts, many=True)
        return JsonResponse(posts_serializer.data, safe=False)
    
    elif request.method == 'POST': 
        post_data = JSONParser().parse(request)
        post_serializer = PostSerializer(data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse(post_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def post_detail(request, slug):
    
    try: 
        post = Post.objects.get(slug=slug) 
    except Post.DoesNotExist: 
        return JsonResponse({'message': 'The post does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET': 
        post_serializer = PostSerializer(post) 
        return JsonResponse(post_serializer.data) 
    
    elif request.method == 'PUT': 
        post_data = JSONParser().parse(request) 
        post_serializer = PostSerializer(post, data=post_data) 
        if post_serializer.is_valid(): 
            post_serializer.save() 
            return JsonResponse(post_serializer.data) 
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    elif request.method == 'DELETE': 
        post.delete() 
        return JsonResponse({'message': 'Post was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
