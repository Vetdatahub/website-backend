from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import Profile, User


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "profile", "joined_date", "first_name", "last_name"]


class RegisterUserSerializer(ModelSerializer):
    affiliation = serializers.CharField(max_length=200, required=False)
    role = serializers.ChoiceField(choices=Profile.ROLES_CHOICES)
    subscribe_to_newsletter = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "affiliation",
            "role",
            "subscribe_to_newsletter",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        affiliation = validated_data.pop("affiliation")
        role = validated_data.pop("role")
        subscribe_to_newsletter = validated_data.pop("subscribe_to_newsletter")
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(
            user=user, affiliation=affiliation, role=role, subscribe_to_newsletter=subscribe_to_newsletter
        )
        return user


class ProfileSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ["user"]  # prevent user field from being updated
