from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
from rest_framework import serializers

class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()