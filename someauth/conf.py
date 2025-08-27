from django.conf import settings

DEFAULTS = {
    "USE_SOCIAL": False,   
    "ENABLED_PROVIDERS": [],  # nothing enabled
    "PROVIDERS": {},  # no client ids/secrets
    "EMAIL_VERIFICATION": "optional",  # can override Allauth behavior
    "LOGIN_REDIRECT_URL": "/",  # safe default
}

def get_quickauth_setting(key):
    """
    Fetch a QuickAuth setting from Django settings, 
    falling back to sensible defaults if missing.
    """
    return getattr(settings, "SOMEAUTH", {}).get(key, DEFAULTS.get(key))

def enforce_socialaccount_consistency():
    """
    Enforce consistency for social login setup.
    Raises RuntimeError if:
      - USE_SOCIAL=True but required apps are missing
      - USE_SOCIAL=True but no providers enabled
      - USE_SOCIAL=True but enabled providers have missing credentials
    """
    someauth = getattr(settings, "SOMEAUTH", {})
    use_social = someauth.get("USE_SOCIAL", True)

    if not use_social:
        return  # nothing to enforce

    enabled_providers = someauth.get("ENABLED_PROVIDERS", [])
    providers_config = someauth.get("PROVIDERS", {})

    # --- Check that at least one provider is enabled ---
    if not enabled_providers:
        raise RuntimeError(
            "QuickAuth: USE_SOCIAL=True but 'ENABLED_PROVIDERS' is empty. "
            "Specify at least one provider to enable social login."
        )

    # --- Check credentials for each enabled provider ---
    missing_creds = []
    for provider in enabled_providers:
        creds = providers_config.get(provider)
        if not creds or not creds.get("client_id") or not creds.get("secret"):
            missing_creds.append(provider)
    if missing_creds:
        raise RuntimeError(
            f"QuickAuth: The following enabled providers are missing "
            f"client_id or secret in 'PROVIDERS': {missing_creds}"
        )

    # --- Check required INSTALLED_APPS ---
    required_apps = ["allauth.socialaccount"] + [
        f"allauth.socialaccount.providers.{provider}" for provider in enabled_providers
    ]
    missing_apps = [app for app in required_apps if app not in settings.INSTALLED_APPS]
    if missing_apps:
        raise RuntimeError(
            f"QuickAuth: USE_SOCIAL=True but the following apps are missing "
            f"from INSTALLED_APPS: {missing_apps}. "
            "Please add them to enable social login."
        )