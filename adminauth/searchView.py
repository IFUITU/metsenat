from rest_framework.views import APIView
from .models import Patron, Student
from .serializers import PatronSerializer, StudentSerializerGET
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response
from .filters import PatronFilter, StudentFilter

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def searchPatron(request):
    try:
       query = Patron.objects.all()
    except Patron.DoesNotExist as ex:
        return Response({"error":dict(ex)})
    filterset = PatronFilter(request.data, queryset=query)

    if not filterset.is_valid():
        return Response({"errors":filterset.errors})
    patrons = PatronSerializer(filterset.qs, many=True)
    return Response({"data":patrons.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def searchStudent(request):
    try:
       query = Student.objects.all()
    except Student.DoesNotExist as ex:
        return Response({"error":dict(ex)})
    filterset = StudentFilter(request.data, queryset=query)
    if not filterset.is_valid():
        return Response({"errors":filterset.errors})
    patrons = StudentSerializerGET(filterset.qs, many=True)
    return Response({"data":patrons.data})



