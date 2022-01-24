from rest_framework import serializers

class StatisticsSerializer(serializers.Serializer):
    payment_sum = serializers.FloatField()
    asked_sum = serializers.FloatField()
    must_pay = serializers.FloatField()
    patrons  = serializers.IntegerField()
    students = serializers.IntegerField()