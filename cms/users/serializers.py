from rest_framework import serializers
from django.contrib.auth.models import update_last_login, Group, Permission
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from .models import CustomUser, Reporter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "email", "password", "first_name", "last_name", "role")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ReporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporter
        fields = ["previous_works", "biography", "verified"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "zipcode"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        try:
            user = CustomUser.objects.get(email=email)
        except:
            raise serializers.ValidationError(
                "The user with the email is not registered."
            )

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                update_last_login(None, user)
                data["user"] = user
                return data
            else:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials."
                )
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

    def create(self, validated_data):
        user = validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return token.key


class UserProfileSerializer(serializers.ModelSerializer):
    reporter = ReporterSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "reporter",
            "password",
        ]
        read_only_fields = ["id", "role", "reporter", "password"]
        permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, validated_data):
        role = validated_data.pop("role", None)
        reporter_data = validated_data.pop("reporter", None)
        user = CustomUser.objects.get(user=validated_data.get("user"))

        if role == CustomUser.REPORTER and reporter_data:
            Reporter.objects.create(user=user, **reporter_data)
            reporter_group = Group.objects.get(name="reporter")
            user.groups.add(reporter_group)
        else:
            user_group = Group.objects.get(name="user")
            user.groups.add(user_group)
        user.is_verified = False
        user.is_active = False
        user.save()
        return user


class RegisterSerializer(CustomUserSerializer):
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    reporter = ReporterSerializer(required=False)

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            "confirm_password",
            "zipcode",
            "reporter",
        )

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match")

        return super().validate(data)

    def create(self, validated_data):
        reporter_data = validated_data.pop("reporter", None)

        user = super().create(validated_data)

        if reporter_data:
            validated_data["role"] = CustomUser.REPORTER
            Reporter.objects.create(user=user, **reporter_data)
            reporter_group = Group.objects.get(name="reporter")
            user.groups.add(reporter_group)
        else:
            validated_data["role"] = CustomUser.USER
            user_group = Group.objects.get(name="user")
            user.groups.add(user_group)

        user.is_verified = False
        user.is_active = False
        user.save()
        return user
