from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _

class ClientSerializer(serializers.ModelSerializer):
    confirm = serializers.CharField(max_length=50,write_only=True)

    def validate(self, data):
        password = data.get("password")
        confirm = data.get("confirm")
        if password != confirm:
            raise serializers.ValidationError("Confirmation password is not valid!")
        return data
        
    class Meta:
        model = User
        fields = ["id","username", "first_name", "last_name", "email", "phone", "password", "confirm", "image"]
        read_only_fields = ("id",)
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ClientSerializerPUT(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "image"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(required=True, max_length=35, min_length=1)
    new = serializers.CharField(required=True, max_length=35, min_length=6, write_only=True)
    confirm = serializers.CharField(required=True, max_length=35, min_length=6, write_only=True)
    

    def validate(self, data):
        error = {}
        if not self.context['request'].user.check_password(data.get("password")):
            error['password'] = _("Password is not valid!")
            raise serializers.ValidationError(error)
        
        if not data.get("new") == data.get("confirm"):
            error['confirm'] = _("New password confirmation is not valid!")
            raise serializers.ValidationError(error)

        return data
        
    class Meta:
        model = User
        fields = ["password", 'new', 'confirm']
