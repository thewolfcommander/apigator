from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class UnauthenticatedUserMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        # Redirect to home if user is already authenticated
        return redirect('core:home')  # replace 'home' with your home view name
