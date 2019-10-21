from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.conf import settings
from django.conf.urls import url, include

app_name = 'api'
urlpatterns = [
    url(r'^graphql', csrf_exempt(GraphQLView.as_view())),
]

if settings.DEBUG:
    urlpatterns += [url(r'^graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True, pretty=True)))]
