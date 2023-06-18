from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import View

from accounts.models import *

from apigator.utils import gpt_requestor, git_manager, social

# Create your views here.
@login_required(login_url='accounts:login')
def home(request):
    integration_query = AccountIntegration.objects.filter(user=request.user)
    context = {}

    if integration_query.exists():
        context['integration'] = True
        if integration_query.first().gpt_integration:
            # Getting required data from User's DB
            organization_id = integration_query.first().gpt_integration.organization_id
            key = integration_query.first().gpt_integration.key

            # Initializing GPT Requestor
            requestor = gpt_requestor.GPTRequestor(key, organization_id)

            # Checking for authorization
            authorizor_resp = requestor.check_authorization()
            context['authorized'] = authorizor_resp['status']

            if not authorizor_resp['status']:
                context['authorization_error_message'] = authorizor_resp['message']
    else:
        context['integration'] = False
        context['integration_error_message'] = 'You have not integrated GPT yet.'

    return render(request, 'core/home.html', context)


class CreateGitHubRepo(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        access_token = social.get_user_github_token(request.user)
        repo_name = request.POST.get('repo_name')
        repo_description = request.POST.get('repo_description')

        github_manager = git_manager.GithubManager(access_token, repo_name, repo_description)
        github_manager.create_github_repo()
        return redirect('core:home')