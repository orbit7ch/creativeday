from django.conf import settings


def settings_context(request):
    context = {
        'GOOGLE_TAG_MANAGER_CONTAINER_ID': settings.GOOGLE_TAG_MANAGER_CONTAINER_ID,
        'DEBUG': settings.DEBUG,
        'SITE_NAME': settings.SITE_NAME
    }
    return context
