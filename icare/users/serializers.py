from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    phone_number = PhoneNumberField(required=False)
    avatar = serializers.ImageField(required=False, write_only=True)
    avatar_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "name",
            "email",
            "password",
            "phone_number",
            "token",
            "avatar",
            "avatar_url",
        )

    def get_token(self, obj=None):
        return str(obj.auth_token)

    def get_avatar_url(self, user):
        request = self.context.get("request")
        avatar_url = user.avatar.url
        return request.build_absolute_uri(avatar_url)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField()
    new_password = serializers.CharField()
