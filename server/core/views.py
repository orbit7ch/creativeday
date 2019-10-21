import logging
import os
import urllib
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from graphene_django.views import GraphQLView
import datetime

logger = logging.getLogger(__name__)


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


def access_test(user):
    return not settings.LOGIN_REQUIRED or user.is_authenticated


@user_passes_test(access_test)
@ensure_csrf_cookie
def home(request):
    if settings.DEBUG:
        import socket
        def hostname_resolves(hostname):
            try:
                socket.gethostbyname(hostname)
                return True
            except socket.error:
                return False

        try:
            url = 'http://{}:8080/{}'.format(
                'host.docker.internal' if hostname_resolves('host.docker.internal') else 'localhost',
                request.get_full_path())
            r = requests.get(url)
            return HttpResponse(r.text)
        except Exception as e:
            print('Can not connect to dev server at {} ({})'.format(url, e))

    response = render(request, 'index.html', {})
    if request.user.is_staff:
        response.set_cookie('i_am_internal', 'true', expires=datetime.datetime(2099, 1, 1))

    return response


def i_am_internal(request):
    response = HttpResponseRedirect('/')
    response.set_cookie('i_am_internal', 'true', expires=datetime.datetime(2099, 1, 1))

    return response


def legacy_search(request, query):
    d = {k: v for k, v in request.GET.items()}
    d['q'] = query
    return HttpResponsePermanentRedirect('/search?{}'.format(urllib.parse.urlencode(d)))
