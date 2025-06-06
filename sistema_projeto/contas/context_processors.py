from django.conf import settings

def admin_emails(request):
    return {
        'ADMIN_EMAILS': settings.ADMIN_EMAILS
    }
