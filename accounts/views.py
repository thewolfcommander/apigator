from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import FormView

from .forms import UserLoginForm, UserRegisterForm
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
