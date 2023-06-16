from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import UserLoginForm, UserRegisterForm
from .mixins import UnauthenticatedUserMixin

class UserLoginView(UnauthenticatedUserMixin, FormView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:home')  # Change this to your desired URL

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class UserRegisterView(UnauthenticatedUserMixin, FormView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:home')  # Change this to your desired URL

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
