# views.py
from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

class UsersWithoutGithubView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.exclude(id__in=SocialAccount.objects.filter(provider='github').values('user'))
