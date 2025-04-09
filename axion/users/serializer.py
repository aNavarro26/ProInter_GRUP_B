from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "full_name",
            "email",
            "password",
            "address",
            "role",
        ]
        extra_kwargs = {"password": {"write_only": True}}