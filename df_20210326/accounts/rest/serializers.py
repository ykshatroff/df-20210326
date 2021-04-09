import uuid

from rest_framework import serializers


def generate_password():
    return str(uuid.uuid4())


class UserSerializer(serializers.Serializer):
    """
    Display user
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    active = serializers.BooleanField(default=False)


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(max_length=255, default=generate_password)
