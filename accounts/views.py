from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.views.generic.edit import UpdateView

from .forms import UserAccountUpdateForm, UserLoginForm, UserRegisterForm
from .mixins import UnauthenticatedUserMixin


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('core:home')


class UserLoginView(UnauthenticatedUserMixin, FormView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('core:home')  # Change this to your desired URL

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class UserRegisterView(UnauthenticatedUserMixin, FormView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('core:home')  # Change this to your desired URL

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserAccountUpdateForm
    template_name = 'accounts/my_account.html'
    success_url = reverse_lazy('accounts:my_account')

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['github_connected'] = SocialAccount.objects.filter(user=self.request.user, provider='github').exists()
        return context
