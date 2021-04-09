from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)
    active = serializers.BooleanField(default=False)

