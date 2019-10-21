from django.core.management import BaseCommand
from wagtail.images import get_image_model

from cms.tagging import TAG_ENRICHMENT, I18N_TAGS
from core.utils import overwrite_media_domain


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_image_model().objects.filter(tags__name='delete', collection__name='services').delete()

        for k, v in TAG_ENRICHMENT.items():
            for v1 in v:
                for i in get_image_model().objects.filter(tags__name=k).exclude(tags__name=v1):
                    i.tags.add(v1)

        for tid, text in I18N_TAGS:
            for i in get_image_model().objects.filter(tags__id=tid).exclude(tags__name=text):
                i.tags.add(text)

        for image in get_image_model().objects.all().order_by('id'):
            if image.collection.name == 'services':
                image.make_semantic_tags()
                if image.all_tags_str:
                    image.title = image.all_tags_str[:254]

            image.url_800x800 = overwrite_media_domain(image.get_rendition('max-800x800|format-jpeg').url)
            image.url_400x400 = overwrite_media_domain(image.get_rendition('max-400x400|format-jpeg').url)
            image.url_200x200 = overwrite_media_domain(image.get_rendition('max-200x200|format-jpeg').url)

            # wagtail admin interface
            image.get_rendition('max-165x165|format-jpeg')

            image.save()
