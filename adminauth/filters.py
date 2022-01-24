from django_filters import rest_framework as filters
from .models import Patron, Student

class PatronFilter(filters.FilterSet):
    class Meta:
        model = Patron
        fields = {
            'condition':['exact'], 
            'payment':['exact'], 
            'create_at':['exact']
        }

class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            "student_type":['exact'],
            "OTM":['exact']
        }