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
from .models import AccountIntegration, GPTIntegration
from .mixins import UnauthenticatedUserMixin

from apigator.utils.logger import log_info, log_custom_error

import json


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

        integration_query = AccountIntegration.objects.filter(user=self.request.user)

        if integration_query.exists():
            context['integration_exists'] = True

            if integration_query.first().gpt_integration:
                context['gpt_integration_key'] = integration_query.first().gpt_integration.key
                context['organization_id'] = integration_query.first().gpt_integration.organization_id
        else:
            context['integration_exists'] = False
        return context


class ConnectGithubView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect('socialaccount_connections')  # This is the url name for the Django AllAuth connections view
    

class DisconnectGithubAccount(View):
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            social_account = SocialAccount.objects.get(user=user, provider='github')
            social_account.delete()

            user.github_account_linked = False
            user.save()

            return redirect('accounts:my_account')

        except SocialAccount.DoesNotExist:
            return redirect('accounts:my_account')

        except Exception as e:
            return redirect('accounts:my_account')


class UpdateIntegrationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        key = request.POST.get("key")
        organization_id = request.POST.get('org_id')
        integration_query = AccountIntegration.objects.filter(user=self.request.user)
        if integration_query.exists():
            integration_obj = integration_query.first()
        else:
            integration_obj = AccountIntegration.objects.create(user=self.request.user)

        if integration_obj.gpt_integration:
            integration_obj.gpt_integration.key = key
            integration_obj.gpt_integration.organization_id = organization_id
            integration_obj.gpt_integration.save()

            # create activity
            # activity = json.loads(integration_obj.activity
        else:
            gpt_integration = GPTIntegration.objects.create(key=key, organization_id=organization_id)
            integration_obj.gpt_integration = gpt_integration
            integration_obj.save()

        return redirect('accounts:my_account')
