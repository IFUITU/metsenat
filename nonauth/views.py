
from adminauth.models import Patron
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from adminauth.serializers import PatronSerializer
# Create your views here

class ApplicationView(ListCreateAPIView):
    queryset = Patron.objects.all()
    serializer_class = PatronSerializer