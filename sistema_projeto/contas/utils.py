from django.conf import settings

def is_admin(user):
    if not user.is_authenticated:
        return False
    return user.email in getattr(settings, 'ADMIN_EMAILS', [])
