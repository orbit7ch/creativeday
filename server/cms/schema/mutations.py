import json

import graphene
from django.core.exceptions import ValidationError
from graphene import InputObjectType, relay
from taggit.models import Tag
from wagtail.images import get_image_model

from api.utils import get_errors, get_object, update_create_instance
from cms.models import UserSearchTerm
from cms.schema import ImageNode, TagNode
from core.middleware import get_current_user, get_current_request


class ImageUpdateInput(InputObjectType):
    title = graphene.String(required=False)
    tag_slugs = graphene.String(required=False)


class UpdateImage(relay.ClientIDMutation):
    class Input:
        image = graphene.Argument(ImageUpdateInput)
        id = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    updated_image = graphene.Field(ImageNode)
    tags = graphene.List(TagNode)

    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):

        u = get_current_user()

        if u.is_superuser:
            try:
                image_instance = get_object(get_image_model(), kwargs['id'])
                if image_instance:
                    image_data = kwargs.get('image')
                    updated_image = update_create_instance(image_instance, image_data, exception=['id', 'tags'])
                    tag_slugs = image_data.get('tag_slugs', '')
                    if tag_slugs is not None:
                        tag_slugs = [t.strip() for t in tag_slugs.split(',') if t.strip()]
                        tags = list(Tag.objects.filter(slug__in=tag_slugs))
                        tag_slugs = [t for t in tag_slugs if t not in [e.slug for e in tags]]
                        updated_image.tags.set(*(tags + tag_slugs))

                    if updated_image.pk:
                        return cls(updated_image=updated_image, tags=Tag.objects.all())
            except ValidationError as e:
                errors = get_errors(e)
            except Exception as e:
                errors = ['Error: {}'.format(e)]
            else:
                errors = ['image not found']

        return cls(updated_image=None, tags=None, errors=errors)


class UserSearchTermInput(InputObjectType):
    data = graphene.String(required=True)


class StoreUserSearchTerm(relay.ClientIDMutation):
    class Input:
        term = graphene.Argument(UserSearchTermInput)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):

        request = get_current_request()

        try:
            is_internal = request.COOKIES.get('i_am_internal', False) != False

            term = kwargs.get('term')
            UserSearchTerm.objects.create(
                session_id=request.session.session_key if request else None,
                ga_id=request.COOKIES.get('_ga', '') if request else None,
                fields=json.loads(term.data),
                is_internal=is_internal,
                reported=is_internal  # do not report internal searches
            )
        except Exception as e:
            errors = ['Error: {}'.format(e)]
        except ValidationError as e:
            errors = get_errors(e)
        else:
            errors = []

        return cls(errors=errors)
