from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "password", "is_active"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "id": {"read_only": True},
            "is_active": {"required": False},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)
