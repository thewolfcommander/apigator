from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path('my_account/', views.UserAccountUpdateView.as_view(), name='my_account'),
    path("register/", views.UserRegisterView.as_view(), name="register"),
]
