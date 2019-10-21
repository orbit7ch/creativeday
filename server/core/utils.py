import json
import uuid
from urllib.parse import urlunparse, urlparse

from django.conf import settings
from django.utils.crypto import get_random_string
import time
import datetime
import logging
import random
import string

logger = logging.getLogger(__name__)


def random_id(length=8):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length)])


def get_timestamp_now(a_datetime=None):
    if not a_datetime:
        a_datetime = datetime.datetime.now()

    return int(time.mktime(a_datetime.timetuple()))


def pretty_print(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))


def add_items_to_key(dict, key, items):
    if key in dict:
        dict[key].extend(items)
    else:
        dict[key] = items


def get_random_secret(str_length=32):
    return '{}-{}'.format(get_random_string(str_length), uuid.uuid4())


def overwrite_media_domain(url):
    if settings.OVERWRITE_MEDIA_DOMAIN:
        return urlunparse(urlparse(url)._replace(netloc=settings.OVERWRITE_MEDIA_DOMAIN))

    return url
