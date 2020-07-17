from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

from .views import *

app_name = 'users'

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name="signup"),
    path('my_profile/', MyProfileView.as_view(), name="my_profile"),
    path('users/', UsersListView.as_view(), name="users"),
   	path('', TemplateView.as_view(template_name="users/home.html"), name="dashboard"),
   	path('follow/', FollowApiView.as_view(), name="follow_user"),
   	path('unfollow/', UnFollowApiView.as_view(), name="unfollow_user"),
]
