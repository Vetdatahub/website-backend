from rest_framework.serializers import ModelSerializer
from accounts.models import User, Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserDetailSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'joined_date', 'first_name', 'last_name']


