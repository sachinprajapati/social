from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from django.views.generic.edit import CreateView, FormView
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import *
from .serializers import *
from .helpers import *

UserModel = get_user_model()


class CreateUserView(CreateAPIView):
	model = UserModel
	queryset = UserModel.objects.all()
	serializer_class = UserCreateSerializer
	permission_classes = (AllowAny,)


class MyProfileView(LoginRequiredMixin, TemplateView):
	template_name = "users/my_profile.html"

class UsersListView(LoginRequiredMixin, ListView):
	model = UserModel
	template_name = "users/users_list.html"

	def get_queryset(self, *args, **kwargs):
		return self.model.objects.exclude(pk=self.request.user.id)

class FollowApiView(CreateAPIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		data = request.data
		if not data.get('follow_to'):
			return Response({'error': "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			follow_to = get_object_or_404(UserModel, pk=data["follow_to"])
			if Follow.objects.filter(by=request.user, to=follow_to).exists():
				return Response({'error': 'user already followed this user'}, status=status.HTTP_400_BAD_REQUEST)
			elif request.user == follow_to:
				return Response({'error': "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
			else:
				f = Follow(by=request.user, to=follow_to)
				f.save()
				return Response({'status': True}, status=status.HTTP_201_CREATED)


class UnFollowApiView(CreateAPIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		data = request.data
		if not data.get('follow_to'):
			return Response({'error': "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			follow_to = get_object_or_404(UserModel, pk=data["follow_to"])
			if Follow.objects.filter(by=request.user, to=follow_to).exists():
				Follow.objects.filter(by=request.user, to=follow_to).delete()
				return Response({'status': True}, status=status.HTTP_201_CREATED)				
			else:
				return Response({'error': "you are not following to this user"}, status=status.HTTP_400_BAD_REQUEST)
