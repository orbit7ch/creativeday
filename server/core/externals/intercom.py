# -*- coding: utf-8 -*-
#
# Created on 1/25/17 by maersu
import json
from django.conf import settings
from django.utils import translation
import requests
import logging
from django.template.loader import render_to_string
from core.utils import random_id, get_timestamp_now
from intercom.client import Client

logger = logging.getLogger(__name__)


class IntercomApi(object):
    @staticmethod
    def get_client():
        return Client(personal_access_token=settings.INTERCOM_ACCESS_TOKEN)

    @classmethod
    def post_raw(cls, url, data):
        return requests.post(
            url,
            data=json.dumps(data),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer  %s' % settings.INTERCOM_ACCESS_TOKEN
            }
        )

    @classmethod
    def post_user(cls, user):
        """
        create or updates intercom
        """

        if not user.id:
            # intercom needs a user ID to save
            return

        custom_attributes = {
            "last_city": getattr(user, 'city', getattr(user, 'last_city', None)),
            "language": user.language,
            "newsletter": user.newsletter,
            "gender": user.salutation,
            "salutation_de": u"Liäbi" if user.salutation == "w" else u"Liäbä"
        }

        if hasattr(user, 'custom_attributes'):
            custom_attributes.update(user.custom_attributes)

        params = dict(
            email=user.email,
            name=user.get_full_name(),
            phone=user.get_phone(),
            signed_up_at=get_timestamp_now(),
            custom_attributes=custom_attributes
        )

        # multiple users can have the same intercom user so use the intercom_id if possible
        if user.intercom_id:
            params['id'] = user.intercom_id
        else:
            params['user_id'] = user.id

        logger.info('post_user %s' % params)

        if not settings.INTERCOM_ACCESS_TOKEN:
            return random_id()

        try:
            u = cls.get_client().users.create(**params)
            user_tags = [t.name for t in getattr(u, 'tags', [])]

            # tagging user
            if user.categories:
                for c in set(user.categories) - set(user_tags):
                    cls.tags(c, [{'id': user.intercom_id}] if user.intercom_id else [{'user_id': user.id}])

            # Untagging would also delete manual given tags ...
            #
            #     untag = set(user_tags) - set(user.categories)
            # else:
            #    untag = user_tags
            # untag obsolete tags
            # for c in untag:
            #    cls.tags(c, [{'id': user.intercom_id, "untag": True}] if user.intercom_id else [
            #        {'user_id': user.id, "untag": True}])

            return getattr(u, 'id', None)
        except:
            logger.exception('could not save user')

    @classmethod
    def get_user(cls, user_id):
        return cls.get_client().users.find(user_id=user_id)

    @classmethod
    def get_user_events(cls, user_id):
        logger.info('get_user_events %s' % user_id)
        if not settings.INTERCOM_ACCESS_TOKEN:
            return []

        return [
            {
                'event_name': e.event_name,
                'created_at': get_timestamp_now(e.created_at),
                'user_id': e.user_id,
            }
            for e in cls.get_client().events.find_all(type='user', user_id=user_id)
        ]

    @classmethod
    def delete_user(cls, user_id):
        logger.info('delete_user %s' % user_id)
        if not settings.INTERCOM_ACCESS_TOKEN:
            return

        try:
            client = cls.get_client()
            client.users.delete(
                client.users.find(user_id=user_id)
            )
        except:
            logger.exception('could not delete user')

    @classmethod
    def merge_users(cls, base_user, others, force=False):
        """
        merges all intercom users into the oldest user
        messages are not merged :(

        no need to INTERCOM_ACCESS_TOKEN as there is no direct call to intercom

        :param base_user:
        :param others:
        :return:
        """

        try:
            new_events = []
            new_custom_attributes = {}
            obsolete_users = []

            for user in others:
                # skip already merged users (if it's not forced)
                if not force and user.intercom_id == base_user.intercom_id:
                    continue

                try:
                    intercom_user = IntercomApi.get_user(user_id=user.id)
                    events = IntercomApi.get_user_events(user.id)
                    new_custom_attributes.update(intercom_user.custom_attributes)

                    for e in events:
                        e['user_id'] = base_user.id
                        new_events.append(e)

                    obsolete_users.append(user)

                except Exception:
                    logger.exception('%s: %s' % (user.id, e))

            if obsolete_users:
                # that's a hack. so the post signal users overwrites all custom attributes
                base_user.custom_attributes = new_custom_attributes

                # update base user
                base_user_intercom_id = IntercomApi.post_user(base_user)
                IntercomApi.bulk_events(new_events)

                # clean up obsolete intercom users
                for u in obsolete_users:
                    u.intercom_id = base_user.intercom_id
                    u.save()
                    IntercomApi.delete_user(u.id)

                from core.models import CommonLog
                CommonLog.create_log('merge intercom users', data={
                    'base_user_id': base_user.id,
                    'base_user_intercom_id': intercom_user.id,
                    'obsolete_users': [u.id for u in obsolete_users],
                    'migrated_events': len(new_events)
                })

        except:
            logger.exception('could not merge users')

    @classmethod
    def tags(cls, tag, users_dict_list):
        """

        :param tag:
        :param users_dict_list: a list with user objects (https://developers.intercom.com/v2.0/reference#tag-or-untag-users-companies-leads-contacts)
        :return:
        """
        logger.info('tags %s (%s)' % (tag, len(users_dict_list)))
        if not settings.INTERCOM_ACCESS_TOKEN:
            return

        try:
            r = cls.post_raw('https://api.intercom.io/tags', {"name": tag, "users": users_dict_list})
            if not (200 <= r.status_code <= 299):
                logger.error('could not create tags: %s' % getattr(r, 'text', r))
        except:
            logger.exception('could not create tags')

    @classmethod
    def bulk_events(cls, event_list):
        logger.info('bulk_events (%s)' % len(event_list))
        if not settings.INTERCOM_ACCESS_TOKEN:
            return

        try:
            r = cls.post_raw(
                'https://api.intercom.io/bulk/events',
                {
                    "items": [
                        {
                            "method": "post",
                            "data_type": "event",
                            "data": e} for e in event_list
                    ]
                }
            )
            if not (200 <= r.status_code <= 299):
                logger.error('could not create events: %s' % getattr(r, 'text', r))
        except:
            logger.exception('could not create events')

    @classmethod
    def send_email(cls, subject, user, template, context, from_id=settings.INTERCOM_FROM_ID):
        context['host'] = settings.HOST_NAME
        context['first_name'] = user.first_name

        current_language = translation.get_language()
        try:
            translation.activate(user.language)
            body = render_to_string(template, context)
        finally:
            translation.activate(current_language)

        logger.info(u'send_email: %s - %s' % (user.id, subject))

        if not settings.INTERCOM_ACCESS_TOKEN:
            logger.info(u'%s' % body)
            return

        if not settings.INTERCOM_API_ID:
            raise Exception('Could send email - Intercom Application ID not defined')

        try:
            cls.get_client().messages.create(**{
                "message_type": "email",
                "subject": '%s' % subject,
                "body": body,
                "template": "personal",
                "from": {
                    "type": "admin",
                    "id": from_id
                },
                "to": {
                    "type": "user",
                    "user_id": user.id,
                }
            })
        except:
            logger.exception('Could send email')

    @classmethod
    def post_lead(cls, params):
        logger.info('post lead %s' % params)
        if not settings.INTERCOM_ACCESS_TOKEN:
            return

        try:
            return cls.post_raw('https://api.intercom.io/contacts', params)
        except:
            logger.exception('could not post lead')
