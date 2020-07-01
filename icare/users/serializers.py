from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    phone_number = PhoneNumberField(required=False)

    class Meta:
        model = CustomUser
        fields = ("name", "email", "password", "phone_number", "token")

    def get_token(self, obj=None):
        return str(obj.auth_token)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField()
    new_password = serializers.CharField()
