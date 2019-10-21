import logging
from urllib.parse import urlparse

from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
import re

from wagtail.contrib.redirects.middleware import get_redirect

logger = logging.getLogger(__name__)

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()


def get_current_request():
    """ returns the request object for this thread """
    return getattr(_thread_locals, "request", None)


def get_current_user():
    """ returns the current user, if exist, otherwise returns None """
    request = get_current_request()
    if request:
        return getattr(request, "user", None)


class ThreadLocalMiddleware(MiddlewareMixin):
    """ Simple middleware that adds the request object in thread local storage."""

    def process_request(self, request):
        _thread_locals.request = request

    def process_response(self, request, response):
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        return response


class CommonRedirectMiddleware(MiddlewareMixin):
    """
    redirects common bad requests or missing images
    """
    DEFAULT_REDIRECTS = [
        (re.compile("(?i)(.+\.php|.+wp-admin.+|.+\.htm|\/wordpress\/|\/wp\/|\/mm5\/|\/wp-content\/)"),
         'http://example.org/'),
    ]

    def process_request(self, request):
        # FIXME remove it after a while:
        if 'heroku' in request.get_host():
            return redirect(settings.BASE_URL + request.path)

        if not settings.DEBUG:
            try:
                host_name = request._get_raw_host()

                # link shortener?
                if host_name.startswith('get.'):
                    path = request.get_full_path().lower()
                    # Get the path without the query string or params
                    # and check for a wagtail redirect
                    redirect_object = get_redirect(request, urlparse(path).path)
                    if redirect_object:
                        return redirect(redirect_object.link, redirect_object.is_permanent)

                    # no redirect found do an ordinary redirect to main page
                    return redirect(settings.BASE_URL + request.get_full_path(), permanent=False)

                if not host_name.startswith(settings.BASE_HOST_NAME):
                    return redirect(settings.BASE_URL + request.get_full_path(), permanent=False)

            except Exception as e:
                logger.exception('Can not redirect')

    def process_exception(self, request, exception):
        if exception.__class__ == Http404:
            new_path = self.not_found(request)
            if new_path:
                return redirect(new_path, permanent=True)

    def process_response(self, request, response):
        if response.status_code == 404:
            new_path = self.not_found(request)
            if new_path:
                return HttpResponsePermanentRedirect(new_path)

        return response

    def not_found(self, request):
        path = request.get_full_path().lower()
        # generic stuff
        for re_pattern, to in self.DEFAULT_REDIRECTS:
            if re_pattern.match(path):
                return to

        if settings.USE_404_FALLBACK_IMAGE:
            # some static image is missing show a placeholder (use full for local dev)
            m = re.match(r".*(max|fill)-(?P<dimensions>\d+x\d+)\.(jpg|png|svg)", path)
            if m:
                return 'https://picsum.photos/{}'.format(m.group('dimensions').replace('x', '/'))
                # or dummy image: return 'http://via.placeholder.com/{}'.format(m.group('dimensions'))
            if '.png' in path or '.jpg' in path or '.svg' in path or 'not-found' in path:
                return 'https://picsum.photos/400/400'
