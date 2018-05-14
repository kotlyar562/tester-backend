from rest_framework import serializers
from djoser.serializers import UserSerializer
from src.accounts.models import User


class UserInfoSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('email', 'user_id', 'first_name', 'last_name')
        read_only_fields = ('user_id',)


