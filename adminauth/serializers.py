from dataclasses import fields
from gettext import install
from .models import OTM, Patron, Student, PatronToStudent
from rest_framework import serializers

class PatronSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patron
        fields = "__all__"
        depth = 1
        read_only_fields = ('id',)

    
class OTMSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTM
        fields = "__all__"
        read_only_fields = ('id',)

class StudentSerializerGET(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"
        depth = 1

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ('id',)


class PatronToStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatronToStudent
        fields = "__all__"
        read_only_fields = ('id',)

class PatronToStudentSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = PatronToStudent
        fields = "__all__"
        depth = 1 #works only for read 
        