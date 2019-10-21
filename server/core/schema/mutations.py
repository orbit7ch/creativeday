import json

import graphene
from django.core.exceptions import ValidationError
from graphene import InputObjectType, relay

from api.utils import get_errors
from core.middleware import get_current_request
from core.models import GenericEvent


class EventInput(InputObjectType):
    title = graphene.String(required=True)
    data = graphene.String(required=True)


class StoreEvent(relay.ClientIDMutation):
    class Input:
        event = graphene.Argument(EventInput)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):
        request = get_current_request()

        try:
            event = kwargs.get('event')
            GenericEvent.objects.create(
                title=event.title,
                fields=json.loads(event.data),
                session_id=request.session.session_key if request else None,
                ga_id=request.COOKIES.get('_ga', '') if request else None,
                is_internal=request.COOKIES.get('i_am_internal', False) != False
            )
        except Exception as e:
            errors = ['Error: {}'.format(e)]
        except ValidationError as e:
            errors = get_errors(e)
        else:
            errors = []

        return cls(errors=errors)
