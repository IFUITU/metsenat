from dataclasses import fields
from gettext import install
from .models import OTM, Patron, Student, PatronToStudent
from rest_framework import serializers

class PatronSerializer(serializers.ModelSerializer):
    remainder_payment = serializers.ReadOnlyField()
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


class StudentSerializer(serializers.ModelSerializer):
    remainder_contract = serializers.ReadOnlyField()
    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ('id',)


class PatronToStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatronToStudent
        fields = "__all__"
        read_only_fields = ('id',)

    def validate(self, data):
        """
        Check sums of patron and student is enought
        """
        try:
            patron = data['patron']
            student = data['student']
        except Exception as ex:
            raise serializers.ValidationError(ex)

        if data['payed'] > patron.remainder_payment:
            raise serializers.ValidationError(
                "You have {} not enought to pay {}!".format(patron.remainder_payment,data['payed'])
            )
        elif data['payed'] > student.remainder_contract:
            raise serializers.ValidationError(
                "Student needs {} you payed {}!".format(student.remainder_contract, data['payed'])
            )
        return data


class PatronToStudentSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = PatronToStudent
        fields = "__all__"
        depth = 1 #works only for read 
