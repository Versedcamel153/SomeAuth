# someauth/signals.py
from django.db import transaction
from django.db.models.signals import post_migrate
from django.apps import apps
from .conf import get_quickauth_setting
import logging

logger = logging.getLogger(__name__)

def setup_socialapps(sender, **kwargs):
    use_social = get_quickauth_setting("USE_SOCIAL")
    if not use_social:
        return  # social login disabled

    enabled = get_quickauth_setting("ENABLED_PROVIDERS") or []
    providers = get_quickauth_setting("PROVIDERS") or {}

    if not enabled:
        logger.warning("QuickAuth: USE_SOCIAL=True but ENABLED_PROVIDERS is empty. No SocialApps created.")
        return

    def do_setup():
        try:
            Site = apps.get_model("sites.Site")
            SocialApp = apps.get_model("socialaccount.SocialApp")
        except LookupError:
            logger.warning("QuickAuth: Site or SocialApp model not ready. Skipping social setup.")
            return

        # Create default site if it doesn't exist
        site, _ = Site.objects.get_or_create(
            id=1,
            defaults={"domain": "localhost", "name": "localhost"}
        )

        default_provider_scopes = {
            "google": {"SCOPE": ["profile", "email"], "AUTH_PARAMS": {"access_type": "online"}},
            "github": {"SCOPE": ["user", "repo", "read:org"]},
            "discord": {"SCOPE": ["identify", "email"]},
        }

        # Ensure SOCIALACCOUNT_PROVIDERS dict exists
        if not hasattr(apps.get_app_config("socialaccount"), "providers"):
            setattr(apps.get_app_config("socialaccount"), "providers", {})

        for provider in enabled:
            if provider in default_provider_scopes:
                # set default scopes
                pass  # normally set in settings.py

            creds = providers.get(provider)
            if not creds or not creds.get("client_id") or not creds.get("secret"):
                logger.warning(f"QuickAuth: Provider '{provider}' missing client_id or secret. Skipping.")
                continue

            app, created = SocialApp.objects.get_or_create(
                provider=provider,
                defaults={
                    "name": f"{provider.title()} Login",
                    "client_id": creds["client_id"],
                    "secret": creds["secret"],
                    "key": creds.get("key", ""),
                },
            )
            if not created:
                app.client_id = creds["client_id"]
                app.secret = creds["secret"]
                app.key = creds.get("key", "")
                app.save()

            if site not in app.sites.all():
                app.sites.add(site)

    # Defer until after migrations complete
    transaction.on_commit(do_setup)

post_migrate.connect(setup_socialapps)
