from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model  # If used custom user model

# UserModel = get_user_model()


class RegistraterUserSerializer(serializers.ModelSerializer):
    """
    Serializer used in the registration of a new user.
    """

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        # user = UserModel.objects.create_user(
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user

    class Meta:
        # model = UserModel
        model = User
        fields = (
            "id",
            "username",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}


class UserReturnStringSerializer(serializers.ModelSerializer):
    """
    Returns the string of the object
    """

    class Meta:
        model = User
        fields = (
            "id",
            "get_name",
        )


class UsernameSerializer(serializers.ModelSerializer):
    """
    Returns the username
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )
