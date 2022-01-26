from django.shortcuts import render
from .models import Patron, Student
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import  RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import PatronSerializer, PatronToStudentSerializer, StudentSerializer, PatronToStudent, StudentSerializerGET, PatronToStudentSerializerGET
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
        try:
            student = self.get_object()
        except Student.DoesNotExist:
            return Response({"ok":False,'error':"Student does not exist!"})
        patrons = PatronToStudent.objects.filter(student_id=student.id)
        patron_serialized = PatronToStudentSerializer(patrons, many=True)
        
        serialized = StudentSerializerGET(student, many=False)
        return Response({"ok":True, 'data':serialized.data, "patrons":patron_serialized.data})


class PatronToStudentView(ListCreateAPIView):
    queryset = PatronToStudent.objects.all()
    serializer_class = PatronToStudentSerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        serialized = PatronToStudentSerializerGET(queryset, many=True)
        return Response({"ok":True,"data":serialized.data})
    

class PatronToStudentRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = PatronToStudent.objects.all()
    serializer_class = PatronSerializer

    def get(self, request, pk):
        try:
            query = PatronToStudent.objects.get(pk=pk)
        except PatronToStudent.DoesNotExist as ex:
            return Response({"ok":False,'error':str(ex)})

        serialized = PatronToStudentSerializerGET(query, many=False)
        return Response({"ok":True, 'data':serialized.data})