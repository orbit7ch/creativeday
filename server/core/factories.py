import random

import os
import wagtail_factories
import factory
from django.conf import settings
from django.contrib.auth import get_user_model
from factory.django import ImageField, FileField
from faker import Faker
from taggit.models import Tag
from wagtail.documents.models import get_document_model
from wagtail.images import get_image_model

fake = Faker('de_DE')

def fake_word(*args):
    return fake.word()

def fake_title(*args):
    return fake.sentence(nb_words=random.randint(2, 4)).replace('.', '')


class BasePageFactory(wagtail_factories.PageFactory):
    title = factory.LazyAttribute(fake_title)


class DummyDocumentFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_document_model()

    title = factory.LazyAttribute(fake_title)
    file = FileField(
        from_path=os.path.join(settings.BASE_DIR, 'core', 'static', 'doc', 'dummy.pdf')
    )


class DummyIconFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_document_model()

    title = factory.LazyAttribute(fake_title)
    file = FileField(
        from_path=os.path.join(settings.BASE_DIR, 'core', 'static', 'doc', 'dummy.svg')
    )

def get_image(*args):
    return ImageField(from_path=os.path.join(settings.BASE_DIR, 'core', 'static', 'img', 'dummy',
                                      random.choice(['dummy.jpg', 'dummy1.jpg', 'dummy2.jpg'])))

class DummyImageFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_image_model()

    title = factory.LazyAttribute(fake_title)
    file = ImageField(from_path=os.path.join(settings.BASE_DIR, 'core', 'static', 'img', 'dummy', 'dummy2.jpg'))

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        self.tags.add(*list(Tag.objects.all().order_by('?')[:random.randint(6, 12)]))


# factories.py
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    last_name = factory.LazyAttribute(lambda x: fake.last_name())
    email = factory.LazyAttribute(lambda x: fake.ascii_safe_email())

    @factory.post_generation
    def post(self, create, extracted, **kwargs):
        self.set_password('test')
        self.save()
