from accounts.views import LoginView, RegisterUserView
from django.urls import path
from knox import views as knox_views


urlpatterns = [
    path("login", LoginView.as_view(), name="knox-login"),
    path("logout", knox_views.LogoutView.as_view(), name="knox-logout"),
    path("logoutall", knox_views.LogoutAllView.as_view(), name="knox-logoutall"),
    path("registration", RegisterUserView.as_view(), name="registration"),
]
