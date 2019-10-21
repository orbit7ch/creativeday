import logging
from django.conf import settings
from django.core.management import BaseCommand

from cms.models import UserSearchTerm
from core.externals.slack import SlackApi
from core.models import GenericEvent
from search.query import SearchQuery

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def report_to_slack(
            self,
            klass,
            slack_webhook_url,
            username_callback,
            text_callback,
            enhance_callback=None
    ):
        try:
            for e in klass.objects.filter(reported=False):
                if enhance_callback:
                    enhance_callback(e)

                SlackApi.post_simple_text(
                    username=username_callback(e),
                    text=text_callback(e),
                    slack_webhook_url=slack_webhook_url
                )

                e.reported = True
                e.save()
        except Exception as e:
            logger.exception('Could not report event to slack')

    @staticmethod
    def get_detail(event):
        text = ''
        hostname = 'http://heysmooth.com'
        for k, v in event.fields.items():
            if isinstance(v, list):
                if k == 'urls':
                    value = '\n'.join([hostname + u for u in v])
                else:
                    value = '\n'.join(v)

                text = '{}\n*{}*:\n{}'.format(text, k, value)
            else:
                text = '{}\n*{}*: {}'.format(text, k, v)

        text = '{}\n\n{}'.format(text, event.created)

        if event.is_internal:
            text = '{}\n\n{}'.format(text, 'FROM AN INTERNAL USER')

        return text

    @staticmethod
    def get_search(event):
        search_term = event.fields.get('searchTerm')

        text = '{} ({} results){}'.format(
            search_term,
            event.nbr_results,
            ' - FROM AN INTERNAL USER' if event.is_internal else ''
        )
        return text

    @staticmethod
    def enhance_search(event):
        event.nbr_results = SearchQuery.search(event.fields.get('searchTerm')).count()
        event.has_results = event.nbr_results > 0

    def handle(self, *args, **options):
        self.report_to_slack(
            GenericEvent,
            settings.SLACK_WEBHOOK_URL,
            lambda event: event.title,
            self.get_detail
        )

        self.report_to_slack(
            UserSearchTerm,
            settings.SLACK_WEBHOOK_URL_SEARCH_LOG,
            lambda event: 'User Search',
            self.get_search,
            self.enhance_search
        )
