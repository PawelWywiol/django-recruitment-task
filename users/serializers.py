from typing import ClassVar

from rest_framework import serializers

from .models import User, UserAddress


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields: ClassVar[list[str]] = [
            "id",
            "address_type",
            "valid_from",
            "post_code",
            "city",
            "country_code",
            "street",
            "building_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields: ClassVar[list[str]] = ["id", "created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    addresses = UserAddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields: ClassVar[list[str]] = [
            "id",
            "first_name",
            "last_name",
            "initials",
            "email",
            "status",
            "addresses",
            "created_at",
            "updated_at",
        ]
        read_only_fields: ClassVar[list[str]] = ["id", "created_at", "updated_at"]

    def validate_email(self, value: str) -> str:
        message = "A user with this email already exists."
        if User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(message)
        return value
