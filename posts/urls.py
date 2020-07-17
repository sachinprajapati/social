from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

from .views import *

app_name = 'posts'

urlpatterns = [
    path('home/', HomePage.as_view(), name="homepage"),
   	path('create-post/', CreatePostAPI.as_view(), name="create_post"),
   	path('post-like/', PostLikeAPI.as_view(), name="post_like"),
]
