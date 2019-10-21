import logging
from django.core.management import BaseCommand

from cms.models import UserSearchTerm
from search.query import SearchQuery

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for event in UserSearchTerm.objects.all():
            search_term = event.fields.get('searchTerm')
            nbr_results = SearchQuery.search(search_term).count()

            print('{}: {} -> {}'.format(search_term, event.nbr_results, nbr_results))



