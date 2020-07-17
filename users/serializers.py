from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import *


UserModel = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=True)
	email = serializers.CharField(required=True)

	def create(self, validated_data):
		user = super(UserCreateSerializer, self).create(validated_data)
		user.set_password(validated_data['password'])
		user.save()
		# user = UserModel.objects.create(
		#     username=validated_data['username']
		# )
		# user.set_password(validated_data['password'])
		# user.save()
		p = Profile(user=user)
		p.save()
		return user

	class Meta:
	    model = UserModel
	    fields = ( "email", "username", "password")