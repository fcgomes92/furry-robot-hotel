from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    _cls = serializers.CharField()
    id = serializers.CharField()
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
