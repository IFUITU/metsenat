from django.db.models import Sum
from .serializers import StatisticsSerializer
from rest_framework.views import  APIView
from adminauth.models import Patron, PatronToStudent, Student
from rest_framework.response import Response

class DashApiView(APIView):
    def get(self, request):
        try:
            payed_sum = PatronToStudent.objects.aggregate(Sum("payed"))
            asked_sum = Student.objects.aggregate(Sum("contract_sum"))
        except:
            return Response({"ok":False})
        patrons = Patron.objects.count()
        students = Student.objects.count()
        must_pay = asked_sum['contract_sum__sum'] - payed_sum['payed__sum']
        
        data = {
            "payment_sum":payed_sum['payed__sum'], 
            "asked_sum":asked_sum['contract_sum__sum'], 
            "must_pay":must_pay, 
            "students":students, 
            "patrons":patrons
        }
        serialized = StatisticsSerializer(data, many=False)
        return Response({"ok":True, "data":data})
