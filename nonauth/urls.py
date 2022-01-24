from .views import ApplicationView
from django.urls import path
urlpatterns = [
    path("", ApplicationView.as_view())
]