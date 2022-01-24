
from adminauth.models import Patron
from rest_framework.views import APIView
from rest_framework.response import Response
from adminauth.serializers import PatronSerializer
# Create your views here

class ApplicationView(APIView):
    def get(self, request):
        try:
            query = Patron.objects.all()
        except Patron.DoesNotExist as ex:
            return Response({"ok":False, "error": dict(ex)})
        serialized = PatronSerializer(query, many=True)
        return Response({"data":serialized.data, "ok": True})

    def post(self, request):
        serialized = PatronSerializer(data=request.data, context={"request":request})
        if serialized.is_valid():
            serialized.save()
            return Response({"ok":True, "data":serialized.data})
        return Response({"ok":False, "error":serialized.errors})
