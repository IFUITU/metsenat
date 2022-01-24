from django.shortcuts import render
from .models import Patron, Student
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .serializers import PatronSerializer, PatronToStudentSerializer, StudentSerializer, PatronToStudent, StudentSerializerGET, PatronToStudentSerializerGET
from rest_framework.response import Response
# Create your views here.

class PatronApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            patrons = Patron.objects.all()
        except Patron.DoesNotExist as ex:
            return Response({"error":"Patron does not exist"})
        get_patrons = PatronSerializer(patrons, many=True, context={"request":request})

        return Response({"ok":True,"data":get_patrons.data}, status=200)

    def post(self, request):
        seriallized = PatronSerializer(data=request.data)
        if seriallized.is_valid():
            seriallized.save()
            return Response({"ok":True, "data":seriallized.data})
        return Response({"ok":False, "errors":seriallized.errors})

class PatronRetrieve(APIView):
    def get(self, request, id):
        try:
            patron = Patron.objects.get(id=id)
        except Patron.DoesNotExist:
            return Response({"ok":False,'error':"Patron does not exist!"})

        serialized = PatronSerializer(patron, many=False)
        return Response({"ok":True, 'data':serialized.data})

    def put(self, r, id):
        try:
            patron = Patron.objects.get(id=id)
        except Patron.DoesNotExist as ex:
            return Response({"error":ex})

        serialized = PatronSerializer(instance=patron, data=r.data, context={"request":r})
        print(serialized.initial_data)
        if serialized.is_valid():
            serialized.save()
            return Response({"data":serialized.data,"ok":True}, status=200)
        return Response({"data":serialized.errors,"ok":False})

    def delete(self, request, id):
        try:
            patron = Patron.objects.get(id=id)
        except Patron.DoesNotExist as ex:
            return Response({"ok":False,"error":ex})
        patron.delete()
        return Response({"ok":True, "data":"SUCCESSFULLY DELETED!"})

class StudentApiView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            students = Student.objects.all()
        except Student.DoesNotExist as ex:
            return Response({"error":"Students does not exist"})
        get_students = StudentSerializerGET(students, many=True, context={"request":request})

        return Response({"ok":True,"data":get_students.data}, status=200)

    def post(self, request):
        seriallized = StudentSerializer(data=request.data)
        if seriallized.is_valid():
            seriallized.save()
            return Response({"ok":True, "data":seriallized.data})
        return Response({"ok":False, "errors":seriallized.errors})

class StudentRetrieveView(APIView):

    def get(self, request, id):
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response({"ok":False,'error':"Student does not exist!"})
        patrons = PatronToStudent.objects.filter(student_id=student.id)
        patron_serialized = PatronToStudentSerializer(patrons, many=True)

        serialized = StudentSerializerGET(student, many=False)
        return Response({"ok":True, 'data':serialized.data, "patrons":patron_serialized.data})

    def put(self, r, id):
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist as ex:
            return Response({"error":dict(ex)})

        serialized = StudentSerializer(instance=student, data=r.data, context={"request":r})
        # print(serialized.initial_data)
        if serialized.is_valid():
            # print(serialized.validated_data)
            serialized.save()
            return Response({"data":serialized.data,"ok":True}, status=200)
        return Response({"data":serialized.errors,"ok":False})

    def delete(self, request, id):
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist as ex:
            return Response({"ok":False,"error":dict(ex)})
        student.delete()
        return Response({"ok":True, "data":"SUCCESSFULLY DELETED!"})

class PatronToStudentView(APIView):
    
    def get(self, request):
        try:
            query = PatronToStudent.objects.all()
        except PatronToStudent.DoesNotExist as ex:
            return Response({"error":dict(ex)})
        serialized = PatronToStudentSerializerGET(query, many=True, context={"request":request})

        return Response({"ok":True,"data":serialized.data}, status=200)

    def post(self, request):
        serialized = PatronToStudentSerializer(data=request.data)
        
        if serialized.is_valid():
            serialized.save()
            return Response({"ok":True, "data":serialized.data})
        return Response({"ok":False, "errors":serialized.errors})

class PatronToStudentRetrieveView(APIView):
    def get(self, request, id):
        try:
            query = PatronToStudent.objects.get(id=id)
        except PatronToStudent.DoesNotExist as ex:
            return Response({"ok":False,'error':str(ex)})

        serialized = PatronToStudentSerializerGET(query, many=False)
        return Response({"ok":True, 'data':serialized.data})

    def put(self, r, id):
        try:
            query = PatronToStudent.objects.get(id=id)
        except PatronToStudent.DoesNotExist as ex:
            return Response({"error":dict(ex)})

        serialized = PatronToStudentSerializer(instance=query, data=r.data, context={"request":r})
        print(serialized.initial_data)
        if serialized.is_valid():
            serialized.save()
            return Response({"data":serialized.data,"ok":True}, status=200)
        return Response({"data":serialized.errors,"ok":False})

    def delete(self, request, id):
        try:
            query = PatronToStudent.objects.get(id=id)
        except PatronToStudent.DoesNotExist as ex:
            return Response({"ok":False,"error":dict(ex)})
        query.delete()
        return Response({"ok":True, "data":"SUCCESSFULLY DELETED!"})