from accounts.models import User
from rest_framework import serializers


class RegistraterUserSerializer(serializers.ModelSerializer):
    """
    Serializer used in the registration of a new user.
    """

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user

    class Meta:
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
            "display_name",
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
