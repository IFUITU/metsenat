
from rest_framework.validators import ValidationError
from .models import Patron, Student
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import  RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import PatronSerializer, PatronToStudentSerializer, StudentSerializer, PatronToStudent, PatronToStudentSerializerGET
from rest_framework.response import Response
from rest_framework import status


class PatronApiView(ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Patron.objects.all()
    serializer_class = PatronSerializer


class PatronRetrieve(RetrieveUpdateDestroyAPIView):
    queryset = Patron.objects.all()
    serializer_class = PatronSerializer


class StudentApiView(ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, pk):
        student = self.get_object()
        patrons = PatronToStudent.objects.filter(student_id=student.id)
        patron_serialized = PatronToStudentSerializer(patrons, many=True)
        serialized = StudentSerializer(student, many=False)

        return Response({"ok":True, 'data':serialized.data, "patrons":patron_serialized.data})


class PatronToStudentView(ListCreateAPIView):
    queryset = PatronToStudent.objects.all()
    serializer_class = PatronToStudentSerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        result = self.paginate_queryset(queryset)
        serialized = PatronToStudentSerializerGET(result, many=True)

        return self.get_paginated_response({"ok":True,"data":serialized.data})


class PatronToStudentRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = PatronToStudent.objects.all()
    serializer_class = PatronToStudentSerializer

    def get(self, request, *args, **kwargs):
        query = self.get_object()    
        serialized = PatronToStudentSerializerGET(query, many=False)

        return Response({"ok":True, 'data':serialized.data})
