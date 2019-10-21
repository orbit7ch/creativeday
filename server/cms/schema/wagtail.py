# https://wagtail.io/blog/graphql-with-streamfield/
import django_filters
import graphene
from graphene_django import DjangoObjectType
from taggit.models import Tag
from wagtail.documents.models import Document
from wagtail.images import get_image_model
from graphene_django.converter import convert_django_field


class TagNode(DjangoObjectType):
    class Meta:
        model = Tag
        only_fields = ['name', 'slug']


class ImageRendition(graphene.ObjectType):
    id = graphene.ID()
    url = graphene.String()
    width = graphene.Int()
    height = graphene.Int()


class ImageRenditionList(graphene.ObjectType):
    rendition_list = graphene.List(ImageRendition)
    src_set = graphene.String()

    def resolve_src_set(self, info):
        return ", ".join(
            [f"{img.url} {img.width}w" for img in self.rendition_list])


class ImageFilter(django_filters.FilterSet):
    class Meta:
        model = get_image_model()
        fields = ['title']


class ImageNode(DjangoObjectType):
    tags = graphene.String()

    tags_list = graphene.List(TagNode)

    pk = graphene.Int()
    rating = graphene.Int()

    rendition = graphene.Field(
        ImageRendition,
        max=graphene.String(),
        min=graphene.String(),
        width=graphene.Int(),
        height=graphene.Int(),
        fill=graphene.String(),
        format=graphene.String(),
        bgcolor=graphene.String(),
        jpegquality=graphene.Int()
    )
    rendition_list = graphene.Field(
        ImageRenditionList, sizes=graphene.List(graphene.Int))

    class Meta:
        model = get_image_model()
        only_fields = [
            'title', 'url_800x800', 'url_200x200', 'url_400x400'
        ]
        interfaces = (graphene.relay.Node,)

    def resolve_pk(self, *args, **kwargs):
        return self.id

    def resolve_rating(self, *args, **kwargs):
        return self.rating

    def resolve_tags_list(self, info):
        return self.tags.all()

    def resolve_tags(self, *args, **kwargs):
        return ' <span>/</span> '.join(self.tags.all().values_list('name', flat=True))

    def resolve_rendition(self, info, **kwargs):
        filters = "|".join([f"{key}-{val}" for key, val in kwargs.items()])
        img = self.get_rendition(filters)
        return ImageRendition(id=img.id, url=img.url, width=img.width, height=img.height)

    def resolve_rendition_list(self, info, sizes=[]):
        rendition_list = [
            ImageNode.resolve_rendition(self, info, width=width)
            for width in sizes
        ]
        return ImageRenditionList(rendition_list=rendition_list)


class DocumentNode(DjangoObjectType):
    tags = graphene.List(TagNode)
    url = graphene.String()

    class Meta:
        model = Document
        only_fields = [
            'title'
        ]
        interfaces = (graphene.relay.Node,)
        filter_fields = {}

    def resolve_url(self, *args, **kwargs):
        return self.file.url

    def resolve_tags(self, *args, **kwargs):
        return self.tags.all()

# @convert_django_field.register(Image)
# def convert_image(field, registry=None):
#    return ImageNode(
#        description=field.help_text,
#       required=not field.null
#   )
