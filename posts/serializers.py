from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import *


UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):

	full_name = serializers.CharField(source="get_full_name")

	class Meta:
		model = UserModel
		fields = ('id', 'username', 'email', 'full_name')

class CreateImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Images
		fields = ('img', 'dt')

class getPostSerializer(serializers.ModelSerializer):
	images = CreateImageSerializer(source="images_set", many=True)
	user = UserSerializer()

	class Meta:
		model = Posts
		fields = ('title', 'desc', 'images', 'dt', 'updated_at', 'user')