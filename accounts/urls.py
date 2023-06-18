from django.urls import path

from . import views
from .api import views as api_views

app_name = 'accounts'

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('connect-github/', views.ConnectGithubView.as_view(), name='connect_github'),
    path('disconnect-github/', views.DisconnectGithubAccount.as_view(), name='disconnect_github'),
    path('my_account/', views.UserAccountUpdateView.as_view(), name='my_account'),
    path('register/', views.UserRegisterView.as_view(), name="register"),
    path('update-integration/', views.UpdateIntegrationView.as_view(), name='update_integration'),

    # api views
    path('api/v1/users_without_github/', api_views.UsersWithoutGithubView.as_view(), name='api_users_without_github'),
]
