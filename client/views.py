from .models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import  APIView
from rest_framework.permissions import IsAuthenticated
from .serializer import ClientSerializer, ClientSerializerPUT, ChangePasswordSerializer


class registration(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [~IsAuthenticated]

class LoginApi(APIView):
    permission_classes = [~IsAuthenticated]
    
    def post(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        
        if user is None:
            return Response({"ok":False,'error':"User or password is not valid!"})
        token, create = Token.objects.get_or_create(user=user)
        return Response({"ok":True, "token":token.key, "user":{"username":user.username, 'phone':user.phone,'id':user.id}})

   # @method_decorator(login_required)
    def delete(self, request):
        if request.user.is_authenticated:
            request.auth.delete()
            return Response({"ok":True,"data":"Come back soon!"})
        return Response({"ok":False, "data":"Something wrong!"})


class UserApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user_obj = request.user
        except:
            return Response({"error":"User does not exist"})
        get_user = ClientSerializer(user_obj, many=False, context={"request":request})

        return Response({"ok":True,"user":get_user.data}, status=200)
    
    def put(self, request):
        try:
            user_obj = request.user
        except User.DoesNotExist:
            return Response({"ok":False,'error':"User doew ==s="})

        put_user = ClientSerializerPUT(instance=user_obj, data=request.data)
       
        if put_user.is_valid():
            put_user.save()
            return Response({"ok":True,"data":put_user.data})
        return Response({'data':put_user.errors})

    def patch(self, r):
        try:
            user_obj = r.user
        except User.DoesNotExist:
            return Response({"error":"User not Found!"})

        serialized = ChangePasswordSerializer(instance=r.user, data=r.data, context={"request":r})
        if serialized.is_valid():
            user_obj.set_password(serialized.validated_data.get('new'))
            user_obj.save()
            return Response({"data":serialized.data,"ok":True}, status=200)
        return Response({"data":serialized.errors,"ok":False})

    def delete(self, request):
        try:
            user_obj = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({"error":"User not Found!"})
        user_obj.delete()
        return Response({"ok":True, "data":"Come back!"})

