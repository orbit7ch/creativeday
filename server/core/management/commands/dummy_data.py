import os
import random
import shutil

import wagtail_factories
from decimal import Decimal
from django.conf import settings
from django.core import management
from django.core.management import BaseCommand
from django.db import connection
from wagtail.core.models import Page, Collection
from wagtail.core.rich_text import RichText

from cms.tagging import TRENDING
from core.factories import UserFactory, DummyImageFactory, DummyDocumentFactory, fake_title, fake_word
from cms.factories import PageFactory, TagFactory, CompaniesPageFactory, CompanyPageFactory, OperatorPageFactory, \
    OperatorsPageFactory

KNOW_TAGS = list(set([fake_word().title() for i in range(1, 15)]))

IMAGES_WITH_LABELS = [{'label': t} for t in KNOW_TAGS]
PLAIN_IMAGES = [{'dummy': 'dummy'}] * 6

COORDINATES = [
    {'latitude': Decimal('47.388796'), 'longitude': Decimal('8.486508')},
    {'latitude': Decimal('47.409150'), 'longitude': Decimal('8.545680')},
    {'latitude': Decimal('47.386700'), 'longitude': Decimal('8.528320')},
    {'latitude': Decimal('47.499830'), 'longitude': Decimal('8.729230')},
    {'latitude': Decimal('47.398180'), 'longitude': Decimal('8.451870')},
    {'latitude': Decimal('47.370540'), 'longitude': Decimal('8.517060')},
]

landing_blocks = [
    {'type': 'hero', 'initial': {'space_after': 'pb-4'}},
    {'type': 'text', 'initial': {'space_after': 'pb-4'}},
    {'type': 'button', 'initial': {'space_after': 'pb-4'}},
    {'type': 'text', 'initial': {'space_after': 'pb-4'}},
    {'type': 'swiper', 'initial': {'space_after': 'pb-4', 'images': IMAGES_WITH_LABELS}},
    {'type': 'text', 'initial': {'space_after': 'pb-4'}},
    {'type': 'image', 'initial': {'space_after': 'pb-5'}},
    {'type': 'icon', 'initial': {'space_after': 'pb-0'}},
    {'type': 'text', 'initial': {'space_after': 'pb-5'}},
    {'type': 'icon', 'initial': {'space_after': 'pb-0'}},
    {'type': 'text', 'initial': {'space_after': 'pb-5'}},
    {'type': 'icon', 'initial': {'space_after': 'pb-0'}},
    {'type': 'text', 'initial': {'space_after': 'pb-5'}},
    {'type': 'carousel', 'initial': {'space_after': 'pb-5', 'images': PLAIN_IMAGES}},
    {'type': 'text', 'initial': {'space_after': 'pb-4'}},
    {'type': 'swiper', 'initial': {'space_after': 'pb-4'}},
    {'type': 'text', 'initial': {'space_after': 'pb-4'}},
    {'type': 'button', 'initial': {'space_after': 'pb-5'}},
    {'type': 'tiles', 'initial': {'space_after': 'pb-0', 'images': IMAGES_WITH_LABELS}},
    {'type': 'herotext', 'initial': {'space_after': 'pb-0'}},
    {'type': 'logo', 'initial': {'space_after': 'pb-0'}},
]

service_blocks = [
    {'type': 'carousel', 'initial': {'space_after': 'pb-5', 'images': PLAIN_IMAGES}},
    {'type': 'text', 'initial': {'space_after': 'pb-5'}},
    {'type': 'text', 'initial': {'space_after': 'pb-2',
                                 'text': RichText('<h2>Operators doing #portrait</h2>')}},
    {'type': 'text', 'initial': {'space_after': 'pb-0',
                                 'text': RichText('<h2>More #portrait</h2>')}},
    {'type': 'more', 'initial': {'space_after': 'pb-0'}},
]


class Command(BaseCommand):

    def ensure_clean_dir(self, folder):
        path = os.path.join(settings.MEDIA_ROOT, folder)
        if os.path.exists(path):
            shutil.rmtree(path)
        if not os.path.exists(path):
            os.makedirs(path)

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA IF EXISTS public CASCADE;")
            cursor.execute(
                "CREATE SCHEMA IF NOT EXISTS public AUTHORIZATION {};".format(settings.DATABASES['default']['USER']))
            cursor.execute("GRANT ALL ON SCHEMA public TO postgres;")
        management.call_command('migrate', verbosity=0, interactive=False)

        self.ensure_clean_dir('images')
        self.ensure_clean_dir('original_images')
        self.ensure_clean_dir('documents')

        root = Page.objects.get(title='Root')

        root_coll = Collection.get_first_root_node()
        collection = root_coll.add_child(name='services')

        for i in range(3):
            UserFactory(username='user{}'.format(i))

        TagFactory(name=TRENDING)
        for t in KNOW_TAGS:
            TagFactory(name=t)

        for t in range(10):
            TagFactory()

        for i in range(10):
            DummyImageFactory(
                collection=collection,
                rating=random.choice([0, 1, 2])
            )

        for i in range(3):
            DummyDocumentFactory()

        root_page = PageFactory.create(
            title='Homepage',
            parent=root,
            heading_alignment='center',
            blocks=landing_blocks
        )

        wagtail_factories.SiteFactory.create(
            is_default_site=True,
            root_page=root_page
        )

        Page.objects.filter(slug='home').delete()

        UserFactory(
            username='admin',
            is_staff=True,
            is_superuser=True
        )

        for i in range(1, 4):
            PageFactory.create(
                title='Service {}'.format(i),
                parent=root_page,
                blocks=service_blocks
            )

        PageFactory.create(
            title='Search',
            parent=root_page,
            heading_alignment='center',
            menu_position="main",
            blocks=[
                {'type': 'search', 'initial': {'space_after': 'pb-4',
                                               'filters': [{'text': t} for t in KNOW_TAGS]}},
            ]
        )

        for i in range(1, 8):
            PageFactory.create(
                title=fake_title(),
                heading_alignment='center',
                parent=root_page,
                blocks=landing_blocks,
                menu_position=random.choice(["main", "minor", None])
            )

        PageFactory.create(
            title='Contact',
            parent=root_page,
            heading_alignment='center',
            menu_position="minor",
            blocks=[
                {'type': 'text', 'initial': {'space_after': 'pb-4'}},
                {'type': 'form', 'initial': {'space_after': 'pb-4'}},
            ]
        )

        companies = CompaniesPageFactory.create(parent=root_page, menu_position="main")
        for i in range(1, 5):
            CompanyPageFactory.create(parent=companies, title='Company {}'.format(i), **random.choice(COORDINATES))

        operators = OperatorsPageFactory.create(parent=root_page, menu_position="main")
        for i in range(1, 9):
            OperatorPageFactory.create(parent=operators, title='Operator {}'.format(i))
