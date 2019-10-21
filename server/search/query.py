import re

from django.conf import settings
from wagtail.images import get_image_model
from wagtail.core.models import Collection
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from cms.tagging import TRENDING

pattern = re.compile(r"tat+o+")


class SearchQuery:

    @staticmethod
    def search(text, operator='or', filter_args=None, exclude_args=None):
        if filter_args is None:
            filter_args = {}

        if exclude_args is None:
            exclude_args = {}

        # Get rid of service (since everything is a service ;) )
        text = pattern.sub("", text)

        if not text:
            text = TRENDING

        collection_id = int(settings.SERVICE_COLLECTION_ID if settings.SERVICE_COLLECTION_ID else Collection.objects.get(
            name="services").id)

        searched = get_image_model().objects.filter(
            collection=collection_id, **filter_args
        ).exclude(
            tags__name__in=['nicht in Suche'], **exclude_args
        ).search(
            text,
            operator=operator
        )
        return searched

    @staticmethod
    def suggestions(text):
        """
        concat a string for 'did you mean "XY"?'
        check if there is an option (if not take the original word)
        """
        s = Search(using=Elasticsearch(settings.ELASTIC_URL))
        res = s.suggest('suggestion',
                        text,
                        term={'field': 'all_tags_str'}).execute()

        suggested_words = []
        suggestions = res.suggest['suggestion']

        for ou in suggestions:
            options = ou['options']
            if options:
                suggested_words.append(options[0].text)
            else:
                suggested_words.append(ou['text'])

        suggested = ' '.join(suggested_words)
        if suggested.lower() != text.lower():
            return suggested
