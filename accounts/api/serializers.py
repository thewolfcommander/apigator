# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

class UserSerializer(serializers.ModelSerializer):
    github_connected = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'github_connected']

    def get_github_connected(self, obj):
        return SocialAccount.objects.filter(user=obj, provider='github').exists()
