from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from auth_core.models import CustomUser

class RegisterSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'age']

class RegisterResponseSerializer(ModelSerializer):


    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'age']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
        