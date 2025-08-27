from allauth.account.forms import LoginForm, SignupForm
from allauth.socialaccount.models import SocialAccount
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class CustomLoginForm(LoginForm):
    def clean(self):
        login_input = self.cleaned_data.get("login")

        # Try to fetch user *before* calling super().clean()
        try:
            user = User.objects.get(email__iexact=login_input)

            # Check if it's a social account
            if SocialAccount.objects.filter(user=user).exists():
                raise ValidationError(_("This email is associated with a Google account. Please continue with Google or use the 'Forgot Password' option to set a password."))

            # Check if email is not verified
            if not EmailAddress.objects.filter(user=user, email__iexact=login_input, verified=True).exists():
                raise ValidationError(_("Your email address is not verified yet. Please check your inbox for the verification link to activate your account."))

        except User.DoesNotExist:
            pass  # Let default error handle invalid user

        # Let Allauth handle actual authentication
        return super().clean()
    

class CustomSignupForm(SignupForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_("This email is already in use."))

        if EmailAddress.objects.filter(email__iexact=email).exists():
            raise ValidationError(_("This email is already registered but not verified."))

        return email

    def save(self, request):
        try:
            return super().save(request)
        except IntegrityError:
            raise ValidationError({"email": _("This email is already in use.")})
