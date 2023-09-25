from rest_framework import serializers

from djoser.serializers import UserSerializer as BaseUserSerializer

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = (
            'id', 
            'username', 
            'email',
            'is_superuser',
            'is_staff',
        )


