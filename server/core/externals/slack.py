# -*- coding: utf-8 -*-
#
# Created on 11/3/16 by maersu
import json
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)


class SlackApi(object):
    @staticmethod
    def post_simple_text(text, icon_emoji=None, username=None, slack_webhook_url=settings.SLACK_WEBHOOK_URL):
        if not slack_webhook_url:
            logger.info('post_simple_text\n\n%s' % text)
            return

        args = {"text": text}

        if icon_emoji:
            args['icon_emoji'] = icon_emoji
        else:
            args['icon_emoji'] = ':speech_balloon:'

        if username:
            args['username'] = username

        requests.post(
            slack_webhook_url,
            data=json.dumps(args),
            headers={'Content-Type': 'application/json'}
        )
