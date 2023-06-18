from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path("", views.home, name="home"),
    path("github/create-repo/", views.CreateGitHubRepo.as_view(), name="github_create_repo"),
]
