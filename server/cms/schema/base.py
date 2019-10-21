import logging

import graphene
from graphene.types.generic import GenericScalar
from wagtail.documents.models import Document, get_document_model
from wagtail.images import get_image_model

from wagtail.core.models import Page as WagtailPage
from cms.schema.wagtail import ImageNode, DocumentNode
from cms.models import Page

HOME_SLUG = 'homepage'

logger = logging.getLogger(__name__)


def _get_page_url(page_id):
    if page_id:
        p = WagtailPage.objects.filter(id=page_id).values_list('slug', flat=True)
        if p:
            return '/' + ('' if HOME_SLUG == p[0] else p[0])


class DefaultBlock(graphene.ObjectType):
    block_type = graphene.String()
    value = GenericScalar()


class ImageBlock(DefaultBlock):
    image = graphene.Field(ImageNode)

    def resolve_image(self, info):
        return get_image_model().objects.get(id=self.value.get('image'))


class DocumentBlock(DefaultBlock):
    document = graphene.Field(DocumentNode)

    def resolve_document(self, info):
        return Document.objects.get(id=self.value.get('document'))


class PageContentBlock(DefaultBlock):
    page = GenericScalar()

    def resolve_page(self, info):
        p = Page.objects.get(id=self.value['page'])
        items = []
        for i in p.content.stream_data:
            block_type = i['type']
            if block_type in ['icon', 'text', 'button']:
                i['block_type'] = '{}Block'.format(block_type.title())
                if block_type == 'icon':
                    i['document'] = {'url': Document.objects.get(id=i['value'].get('document')).file.url}
                items.append(i)
        return items


class HeroBlock(DefaultBlock):
    class SlideNode(graphene.ObjectType):
        image = graphene.Field(DocumentNode)
        text = graphene.String()

        def resolve_text(self, info):
            return self.get('text', '')

        def resolve_image(self, info):
            logger.info(self)
            if 'image' in self:
                return get_document_model().objects.get(id=self['image'])
            return None

    slides = graphene.List(SlideNode)
    background_image = graphene.Field(ImageNode)
    button_page_url = graphene.String()

    def resolve_slides(self, info):
        return self.value.get('slides')

    def resolve_background_image(self, info):
        return get_image_model().objects.get(id=self.value.get('background_image'))

    def resolve_button_page_url(self, info):
        return _get_page_url(self.value.get('button_page'))


class SearchBlock(DefaultBlock):
    class FilterNode(graphene.ObjectType):
        image = graphene.Field(ImageNode)
        text = graphene.String()

        def resolve_text(self, info):
            return self['text']

        def resolve_image(self, info):
            return get_image_model().objects.get(id=self['image'])

    filters = graphene.List(FilterNode)

    def resolve_filters(self, info):
        return self.value.get('filters')


class ImageListBlock(DefaultBlock):
    class ItemNode(graphene.ObjectType):
        image = graphene.Field(ImageNode)
        label = graphene.String()
        search_text = graphene.String()
        page_url = graphene.String()

        def resolve_label(self, info):
            return self['label']

        def resolve_search_text(self, info):
            return self['searchText']

        def resolve_image(self, info):
            return get_image_model().objects.get(id=self['image'])

        def resolve_page_url(self, info):
            return _get_page_url(self.get('page'))

    images = graphene.List(ItemNode)

    def resolve_space_after(self, info):
        return self.value.get('space_after')

    def resolve_images(self, info):
        return self.value.get('images')


class TextSearchBlock(DefaultBlock):
    page_url = graphene.String()

    def resolve_page_url(self, info):
        return _get_page_url(self.value.get('page'))


class ButtonBlock(DefaultBlock):
    page_url = graphene.String()

    def resolve_page_url(self, info):
        return _get_page_url(self.value.get('page'))


BLOCKS = {
    'avatar': ImageBlock,
    'image': ImageBlock,
    # 'document': DocumentBlock,
    'icon': DocumentBlock,
    'hero': HeroBlock,
    'herotext': HeroBlock,
    'pagecontent': PageContentBlock,
    'tiles': ImageListBlock,
    'carousel': ImageListBlock,
    'search': SearchBlock,
    'swiper': ImageListBlock,
    'textsearch': TextSearchBlock,
    'button': ButtonBlock,
}


class BlocksList(graphene.Union):
    class Meta:
        types = [DefaultBlock] + list(set(BLOCKS.values()))


class BasePageNodeMixin:
    url = graphene.String()

    @staticmethod
    def resolve_blocks(field):
        repr_content = []
        for block in field.stream_data:
            block_type = block.get('type')
            value = block.get('value')

            klass = BLOCKS.get(block_type, DefaultBlock)
            repr_content.append(klass(value=value, block_type='{}Block'.format(block_type.title())))

        return repr_content

    def resolve_url(self, info):
        return self.url
