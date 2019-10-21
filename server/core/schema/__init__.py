import graphene

from core.schema.mutations import StoreEvent


class CoreMutation(graphene.ObjectType):
    store_event = StoreEvent.Field()
