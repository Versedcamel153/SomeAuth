from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.account.models import EmailAddress
from django.forms import ValidationError
from django.contrib.auth import get_user_model, login
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, resolve_url

User = get_user_model()


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email")
        if not email:
            return  # Let allauth continue its normal flow

        try:
            existing_user = User.objects.get(email=email)

            if sociallogin.is_existing:
                return  # Already linked, let normal flow continue

            # Link the social account to the existing user
            sociallogin.connect(request, existing_user)

            # ✅ Assign backend explicitly
            existing_user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
            login(request, existing_user)

            # ✅ Optional redirect
            raise ImmediateHttpResponse(redirect("dashboard"))  # or any named URL

        except User.DoesNotExist:
            pass  # Let Allauth continue with normal signup

# class CustomAccountAdapter(DefaultAccountAdapter):
#     def get_login_redirect_url(self, request):
#             user = request.user
#             return resolve_url(f'/a/{user.username}/')