from django.urls import path
from .views import LoginApi, registration, UserApiView

urlpatterns = [
    path("Login/", LoginApi.as_view()),
    path("reg-via-admin/", registration.as_view()),
    path("profile/", UserApiView.as_view())
]