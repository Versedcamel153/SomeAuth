from django.conf import settings

def quickauth_settings(request):
    return {
        "QUICKAUTH": getattr(settings, "QUICKAUTH", {})
    }