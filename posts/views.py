from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

UserModel = get_user_model()

class HomePage(LoginRequiredMixin, TemplateView):
	template_name = 'users/home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['posts'] = Posts.objects.filter().order_by('-dt')
		return context

class CreatePostAPI(CreateAPIView):
	permission_classes = [IsAuthenticated]
	parser_classes = (MultiPartParser, FormParser)

	def get(self, request):
	    all_images = Posts.objects.all()
	    serializer = getPostSerializer(all_images, many=True)
	    return JsonResponse(serializer.data, safe=False)

	def post(self, request, *args, **kwargs):
		data = request.data
		if not data.get('desc'):
			return Response({'desc': ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
		images = data.pop('images') if data.get('images') else None
		post = Posts(desc=data['desc'], user=request.user)
		post.save()
		for img in images:
			try:
				i = Images(img=img, post=post)
				i.save()
			except Exception as e:
				print(e)
		return Response({'status': True}, status=status.HTTP_201_CREATED)


class PostLikeAPI(CreateAPIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		data = request.data
		if not data.get('post'):
			return Response({'error': "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			post = get_object_or_404(Posts, pk=data["post"])
			if Like.objects.filter(by=request.user, post=post).exists():
				return Response({'error': 'already added to like'}, status=status.HTTP_400_BAD_REQUEST)				
			else:
				l = Like(post=post, by=request.user)
				l.save()
				return Response({'status': True}, status=status.HTTP_201_CREATED)

