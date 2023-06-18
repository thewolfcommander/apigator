from allauth.socialaccount.models import SocialToken

def get_user_github_token(user):
    # get the social account for the user
    social_account = user.socialaccount_set.get(provider='github')

    print(social_account)
    # get the social token for the account
    token = SocialToken.objects.get(account=social_account)
    return token.token
