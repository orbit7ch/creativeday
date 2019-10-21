import graphene
from django.conf import settings
from graphene_django.debug import DjangoDebug

from cms.schema import CmsQuery, CmsMutation
from core.schema import CoreMutation


class Query(CmsQuery, graphene.ObjectType):
    if settings.DEBUG:
        debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(CmsMutation, CoreMutation, graphene.ObjectType):
    if settings.DEBUG:
        debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
