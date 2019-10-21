import random

import wagtail_factories
from faker import Faker
import factory
from taggit.models import Tag
from wagtail.core.rich_text import RichText
from wagtail.images import get_image_model

from cms.blocks import DocumentBlock, ImageBlock, RichTextBlock, HeroBlock, HeroTextBlock, LogoBlock, TilesBlock, \
    ButtonBlock, SwiperBlock, CarouselBlock, MoreImagesBlock, IconBlock, PlainImageBlock, ReviewBlock, \
    _ServiceItem, SearchBlock, _FilterItem, FormBlock
from cms.models import Page, Companies, Operators, CompanyPage, OperatorPage
from core.factories import BasePageFactory, fake_title, DummyDocumentFactory, DummyImageFactory, DummyIconFactory

fake = Faker('de_DE')


def get_a_page(*args, **kwargs):
    return Page.objects.all().order_by('?').first()


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda x: '{} {}'.format(fake.word().title(), x))


def get_an_image(*args):
    return get_image_model().objects.filter(collection__name='services').order_by('?').first()


# Blocks

class DocumentBlockFactory(wagtail_factories.StructBlockFactory):
    document = factory.SubFactory(DummyDocumentFactory)

    class Meta:
        model = DocumentBlock


class IconBlockFactory(wagtail_factories.StructBlockFactory):
    document = factory.SubFactory(DummyIconFactory)

    class Meta:
        model = IconBlock


class ImageBlockFactory(wagtail_factories.StructBlockFactory):
    image = factory.LazyAttribute(get_an_image)

    class Meta:
        model = ImageBlock


class RichTextBlockFactory(wagtail_factories.StructBlockFactory):
    text = factory.LazyAttribute(lambda x: RichText('<h2>{}</h2>{}'.format(fake_title(), fake.text(max_nb_chars=300))))

    class Meta:
        model = RichTextBlock


class HeroBlockFactory(wagtail_factories.StructBlockFactory):
    background_image = factory.LazyAttribute(get_an_image)
    text = factory.LazyAttribute(fake_title)
    button_link = factory.LazyAttribute(get_a_page)
    button_text = factory.LazyAttribute(fake_title)
    slides = []

    class Meta:
        model = HeroBlock


class HeroTextBlockFactory(wagtail_factories.StructBlockFactory):
    background_image = factory.LazyAttribute(get_an_image)
    text = factory.LazyAttribute(lambda x: RichText(fake.text(max_nb_chars=20)))
    button_link = factory.LazyAttribute(get_a_page)
    button_text = factory.LazyAttribute(fake_title)

    class Meta:
        model = HeroTextBlock


class LogoBlockFactory(wagtail_factories.StructBlockFactory):
    text = factory.LazyAttribute(lambda x: RichText(fake.text(max_nb_chars=30)))

    class Meta:
        model = LogoBlock


class _ServiceItemFactory(wagtail_factories.StructBlockFactory):
    image = factory.LazyAttribute(get_an_image)
    label = factory.LazyAttribute(lambda x: fake_title() if random.choice([True, False]) else None)
    searchText = factory.LazyAttribute(lambda x: fake_title() if random.choice([True, False]) else None)

    class Meta:
        model = _ServiceItem


class _FilterItemFactory(wagtail_factories.StructBlockFactory):
    image = factory.LazyAttribute(get_an_image)
    text = factory.LazyAttribute(lambda x: fake_title() if random.choice([True, False]) else None)

    class Meta:
        model = _FilterItem


class TilesBlockFactory(wagtail_factories.StructBlockFactory):
    images = wagtail_factories.ListBlockFactory(_ServiceItemFactory)

    class Meta:
        model = TilesBlock


class SwiperBlockFactory(TilesBlockFactory):
    class Meta:
        model = SwiperBlock


class CarouselBlockFactory(TilesBlockFactory):
    class Meta:
        model = CarouselBlock


class MoreImagesBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = MoreImagesBlock


class ButtonBlockFactory(wagtail_factories.StructBlockFactory):
    link = factory.LazyAttribute(get_a_page)
    text = factory.LazyAttribute(fake_title)

    class Meta:
        model = ButtonBlock


class PlainImageBlockFactory(wagtail_factories.StructBlockFactory):
    image = factory.LazyAttribute(get_an_image)

    class Meta:
        model = PlainImageBlock


class ReviewFactory(wagtail_factories.StructBlockFactory):
    name = factory.LazyAttribute(lambda x: fake.name_male())
    text = factory.LazyAttribute(lambda x: fake.text(max_nb_chars=240))
    rating = factory.LazyAttribute(lambda x: random.randint(2, 5))

    class Meta:
        model = ReviewBlock


class SearchBlockFactory(wagtail_factories.StructBlockFactory):
    filters = wagtail_factories.ListBlockFactory(_FilterItemFactory)
    tags = []

    class Meta:
        model = SearchBlock


class FormBlockFactory(wagtail_factories.StructBlockFactory):
    form_name = factory.LazyAttribute(fake_title)

    class Meta:
        model = FormBlock


# Pages

factories = {
    'image': ImageBlockFactory,
    'hero': HeroBlockFactory,
    'text': RichTextBlockFactory,
    'herotext': HeroTextBlockFactory,
    'logo': LogoBlockFactory,
    'tiles': TilesBlockFactory,
    'swiper': SwiperBlockFactory,
    'button': ButtonBlockFactory,
    'carousel': CarouselBlockFactory,
    'more': MoreImagesBlockFactory,
    'icon': IconBlockFactory,
    'search': SearchBlockFactory,
    'form': FormBlockFactory
    # 'review': factory
}


def _get_content_item(index, config, field_name='content'):
    base = '{}__{}__{}'.format(field_name, index, config['type'])

    result = {}
    for k, v in config['initial'].items():
        if type(v) == list:
            for i, v2 in enumerate(v):
                for k3, v3 in v2.items():
                    result['{}__{}__{}__{}'.format(base, k, i, k3)] = v3
        else:
            result['{}__{}'.format(base, k)] = v

    return result


class PageFactory(BasePageFactory):
    content = wagtail_factories.StreamFieldFactory(factories)

    class Meta:
        model = Page

    @staticmethod
    def _get_random_content_items():
        return [random.choice(list(factories.keys())) for i in range(0, random.randint(5, 10))]

    @classmethod
    def create(cls, **kwargs):
        blocks = kwargs.pop('blocks', [
            {'type': c, 'initial': {'dummy': 'dummy'}} for c in cls._get_random_content_items()])

        for i, item in enumerate(blocks):
            kwargs.update(_get_content_item(i, item))

        return cls._generate(factory.CREATE_STRATEGY, kwargs)


class CompaniesPageFactory(BasePageFactory):
    title = 'Companies'

    class Meta:
        model = Companies


class OperatorsPageFactory(BasePageFactory):
    title = 'Operators'

    class Meta:
        model = Operators


class CompanyPageFactory(BasePageFactory):
    name = factory.LazyAttribute(lambda x: fake.bs().title())
    street = factory.LazyAttribute(lambda x: fake.street_address())
    zip = factory.LazyAttribute(lambda x: str(random.randint(1000, 8000)))
    city = factory.LazyAttribute(lambda x: fake.city())
    portrait = wagtail_factories.StreamFieldFactory({'image': PlainImageBlockFactory})
    bio = factory.LazyAttribute(lambda x: fake.text(max_nb_chars=240))

    latitude = factory.LazyAttribute(lambda x: fake.latitude())
    longitude = factory.LazyAttribute(lambda x: fake.longitude())

    class Meta:
        model = CompanyPage

    @classmethod
    def create(cls, **kwargs):
        for i, item in enumerate([{'type': 'image', 'initial': {'dummy': 'dummy'}}] * random.randint(2, 4)):
            kwargs.update(_get_content_item(i, item, 'portrait'))

        return cls._generate(factory.CREATE_STRATEGY, kwargs)


class OperatorPageFactory(BasePageFactory):
    pseudonym = factory.LazyAttribute(lambda x: fake.domain_word().title())
    full_name = factory.LazyAttribute(lambda x: fake.name_male())
    bio = factory.LazyAttribute(lambda x: fake.text(max_nb_chars=240))
    companies = factory.LazyAttribute(lambda x: CompanyPage.objects.all().order_by('?')[:random.randint(1, 3)])

    portrait = wagtail_factories.StreamFieldFactory({'image': PlainImageBlockFactory})
    portfolio = wagtail_factories.StreamFieldFactory({'image': PlainImageBlockFactory})
    reviews = wagtail_factories.StreamFieldFactory({'review': ReviewFactory})

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        self.tags.add(*list(Tag.objects.all().order_by('?')[:random.randint(4, 8)]))

    class Meta:
        model = OperatorPage

    @classmethod
    def create(cls, **kwargs):
        for i, item in enumerate([{'type': 'image', 'initial': {'dummy': 'dummy'}}] * random.randint(2, 4)):
            kwargs.update(_get_content_item(i, item, 'portrait'))

        for i, item in enumerate([{'type': 'image', 'initial': {'dummy': 'dummy'}}] * random.randint(3, 9)):
            kwargs.update(_get_content_item(i, item, 'portfolio'))

        for i, item in enumerate([{'type': 'review', 'initial': {'dummy': 'dummy'}}] * random.randint(2, 6)):
            kwargs.update(_get_content_item(i, item, 'reviews'))

        return cls._generate(factory.CREATE_STRATEGY, kwargs)
