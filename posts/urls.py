from . import views
from django.urls import path

urlpatterns = [
    path('api/posts/', views.posts),
    path('api/posts/<slug:slug>/', views.post_detail),
]