from allauth.socialaccount.models import SocialApp, SocialToken, SocialAccount
from .logger import log_info

def get_user_github_token(user, access_token):
    # get the social app for GitHub
    app = SocialApp.objects.get(provider='github')
    # get or create the social account for the user
    social_account, created = SocialAccount.objects.get_or_create(user=user, provider='github')
    # if a new social account was created, also create a social token for it
    if created:
        token = SocialToken.objects.create(app=app, account=social_account, token=access_token)
    else:
        # if the social account already existed, get the existing token
        token = SocialToken.objects.get(account=social_account)

    log_info('github_token_info', data={
        'user': user,
        'token': token,
        'social_account': social_account,
    })
    return token.token
