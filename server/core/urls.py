from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import re_path, path
from django.views.generic import TemplateView
from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.search.urls import admin as wagtailsearch_urls
from wagtail.contrib.sitemaps.views import sitemap
from core import views
from core.views import i_am_internal

re_path

urlpatterns = [
    url(r'^guru/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^cms/', include(wagtailadmin_urls)),
    url('^sitemap\.xml$', sitemap),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    # The included URLconf '<module 'wagtail.search.urls' from '/app/.heroku/python/lib/python3.6/site-packages/wagtail/search/urls/__init__.py'>' does not appear to have any patterns in it. If you see valid patterns in the file then the issue is probably caused by a circular import.
    # url(r'^search/', include(wagtailsearch_urls)),

    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^api/', include('api.urls', namespace="api")),

    # catch as many as possible
    re_path('^ia?m-?internal/?$', i_am_internal),
    path('search/<str:query>', views.legacy_search),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG and not settings.USE_AWS:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # import debug_toolbar
    #
    # urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

# actually we use the cms in headless mode but need the url pattern to get the wagtail_serve function
urlpatterns += [re_path(r'^.*$', views.home, name='home')]

urlpatterns += [url(r'', include(wagtail_urls)), ]

admin.site.site_header = 'Admin'
