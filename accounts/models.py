from django.db import models
from django.contrib.auth.models import User


class GPTIntegration(models.Model):
    """
    GPT integration for user
    """
    key = models.TextField(null=False, blank=False, help_text='GPT integration')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


# Create your models here.
class AccountIntegration(models.Model):
    """
    This model will be used as Integration Bridge Between User and Different Custom Integration Methods
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='Users integration')
    gpt_integration = models.ForeignKey(GPTIntegration, on_delete=models.CASCADE, null=True, blank=True)
    integration_activity = models.JSONField(null=True, blank=True, help_text='For storing connection/re-connection activity')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)