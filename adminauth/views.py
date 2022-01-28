from functools import partial
from rest_framework.validators import ValidationError
from django.shortcuts import get_object_or_404, render
from .models import Patron, Student
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import  RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import PatronSerializer, PatronToStudentSerializer, StudentSerializer, PatronToStudent, PatronToStudentSerializerGET
from rest_framework.response import Response
from rest_framework import status
from .helpers import calculate
from .validators import vlidate_student

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

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        calculate(serializer.data)
        headers = self.get_success_headers(serializer.data)
        

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PatronToStudentRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = PatronToStudent.objects.all()
    serializer_class = PatronToStudentSerializer

    def get(self, request, pk):
        try:
            query = self.get_object()
        except PatronToStudent.DoesNotExist as ex:
            return Response({"ok":False,'error':str(ex)})

        serialized = PatronToStudentSerializerGET(query, many=False)
        return Response({"ok":True, 'data':serialized.data})
    
    def put(self, request, *args, **kwargs):
        kwargs['prev_obj'] = self.get_object()
        serialized = self.get_serializer(instance=self.get_object(), data=request.data)
        serialized.is_valid(raise_exception=True)
        vlidate_student(kwargs['prev_obj'].student, serialized.validated_data['student'])
        self.perform_update(serialized)
        calculate(serialized.data, **kwargs)

        return Response({"ok":True, 'data':serialized.data})
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.patron.payment_sum = obj.patron.payment_sum - obj.payed
        obj.student.payed_sum = obj.student.payed_sum - obj.payed
        obj.patron.save()
        obj.student.save()
        return self.destroy(request, *args, **kwargs)