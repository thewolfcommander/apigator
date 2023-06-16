from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("register/", views.UserLoginView.as_view(), name="register"),
]
