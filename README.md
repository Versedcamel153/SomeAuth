# SomeAuth

A Python package based on **Django Allauth**, simplified to bypass repetitive setup. Comes with **pre-styled Tailwind templates** for quick integration of authentication and social login.

---

## Features

- Email/password authentication.
- Password Reset.
- Email notifications.
- Optional social login (Google, GitHub, Discord, etc.).
- Pre-styled forms using Tailwind CSS with [DaisyUI](https://daisyui.com/).
- Minimal configuration required.
- Supports template overrides for full customization.
- All Allauth views

---

## Installation

```bash
pip install django-someauth
```

Add to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # required

    # SomeAuth
    'someauth',

    # Tailwind (optional)
    'tailwind',
    'theme',

    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Social providers (only include the ones enabled in SOMEAUTH)
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]
```

Set `SITE_ID`:

```python
SITE_ID = 1
```

---

### SomeAuth Configuration

```python
SOMEAUTH = {
    "USE_SOCIAL": True,  # Set False to disable social login
    "ENABLED_PROVIDERS": ["google", "github"],  # Must match provider apps in INSTALLED_APPS
    "PROVIDERS": {
        "google": {
            "client_id": "<your-google-client-id>",
            "secret": "<your-google-secret>",
        },
        "github": {
            "client_id": "<your-github-client-id>",
            "secret": "<your-github-secret>",
        },
    }
}
```

---

## Optional Allauth Settings (Inherited Defaults)

SomeAuth sets sensible defaults for most Allauth settings. You can override them if needed: 

```python
MIDDLEWARE = [
    # default Django middleware
    'allauth.account.middleware.AccountMiddleware',
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "optional"  # or 'mandatory'

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True

ACCOUNT_FORMS = {
    'login': 'someauth.forms.CustomLoginForm',
    'signup': 'someauth.forms.CustomSignupForm',
}
SOCIALACCOUNT_ADAPTER = 'someauth.adapters.MySocialAccountAdapter'
ACCOUNT_ADAPTER = 'someauth.adapters.CustomAccountAdapter'
```

⚠️ Override only when necessary; changing some of these may break SomeAuth behavior.

---

## Email Configuration

SomeAuth supports email notifications. Configure email in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'youraddress@email.com'
EMAIL_HOST_PASSWORD = 'emailpassword'
DEFAULT_FROM_EMAIL = 'youraddress@email.com'  # Should match EMAIL_HOST_USER
```

---

## Template Overrides

To customize the look, create template files matching those in SomeAuth (`someauth/templates/someauth/...`). Django will automatically use your custom templates instead.

---

# First Steps

## URLs

Add SomeAuth URLs to your `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('someauth.urls')),  # handles login, logout, signup, social auth
]
```

## Customization

- Override templates in `templates/someauth/...`
- Override forms via `ACCOUNT_FORMS` in `settings.py`
- Override adapters via `SOCIALACCOUNT_ADAPTER` or `ACCOUNT_ADAPTER`

---

With this setup, your project is fully ready for email/password authentication and optional social login without extra boilerplate.