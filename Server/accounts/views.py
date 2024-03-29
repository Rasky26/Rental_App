from accounts.models import User
from accounts.serializers import RegistraterUserSerializer
from datetime import datetime
from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response


class LoginView(KnoxLoginView):
    """
    Login view. Returns a valid token in the response.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class RegisterUserView(CreateAPIView):
    """
    Registration view. Creates a user and returns a valid token in the response.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistraterUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"registration-errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        token = AuthToken.objects.create(user)
        return Response(
            {
                # "user": UserSerializer(
                #     user, context=self.get_serializer_context()
                # ).data,
                "expiry": AuthToken.objects.get(user=user).expiry.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "token": token[1],
            }
        )
