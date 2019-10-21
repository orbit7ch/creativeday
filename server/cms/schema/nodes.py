import graphene
from graphene_django import DjangoObjectType
from wagtail.images import get_image_model

from cms.models import Page, OperatorPage, CompanyPage
from cms.schema.wagtail import ImageNode, TagNode
from cms.schema.base import BasePageNodeMixin, BlocksList
from search.query import SearchQuery


class PageNode(BasePageNodeMixin, DjangoObjectType):
    content = graphene.List(BlocksList)

    class Meta:
        model = Page
        only_fields = ['id', 'slug', 'title', 'heading_alignment']
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'slug': ['exact', 'icontains', 'in'],
            'title': ['exact', 'icontains', 'in'],
        }

    def resolve_content(self, info):
        # HINT: self.resolve_blocks does not extists
        return BasePageNodeMixin.resolve_blocks(self.content)


class CompanyNode(BasePageNodeMixin, DjangoObjectType):
    operators = graphene.List('cms.schema.nodes.OperatorNode')
    portrait = graphene.List(BlocksList)
    main_portrait = graphene.Field(ImageNode)

    class Meta:
        model = CompanyPage
        only_fields = ['id', 'slug', 'name', 'street', 'zip', 'city', 'bio', 'longitude', 'latitude']
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'slug': ['exact', 'icontains', 'in'],
            'title': ['exact', 'icontains', 'in'],
        }

    def resolve_portrait(self, info):
        return BasePageNodeMixin.resolve_blocks(self.portrait)

    def resolve_operators(self, info):
        return self.operatorpage_set.live().all()

    def resolve_main_portrait(self, *args, **kwargs):
        return get_image_model().objects.get(id=self.portrait.stream_data[0]['value']['image'])


class OperatorNode(BasePageNodeMixin, DjangoObjectType):
    companies = graphene.List(CompanyNode)
    tags = graphene.String()
    main_portrait = graphene.Field(ImageNode)
    portrait = graphene.List(BlocksList)
    portfolio = graphene.List(BlocksList)
    reviews = graphene.List(BlocksList)

    short_bio = graphene.String()

    class Meta:
        model = OperatorPage
        only_fields = ['id', 'slug', 'full_name', 'bio', 'pseudonym']
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'slug': ['exact', 'icontains', 'in'],
            'title': ['exact', 'icontains', 'in'],
        }

    def resolve_tags(self, *args, **kwargs):
        return ' <span>/</span> '.join(self.tags.all().values_list('name', flat=True))

    def resolve_main_portrait(self, *args, **kwargs):
        return get_image_model().objects.get(id=self.portrait.stream_data[0]['value']['image'])

    def resolve_companies(self, info):
        return self.companies.live().all()

    def resolve_portrait(self, info):
        return BasePageNodeMixin.resolve_blocks(self.portrait)

    def resolve_portfolio(self, info):
        return BasePageNodeMixin.resolve_blocks(self.portfolio)

    def resolve_reviews(self, info):
        return BasePageNodeMixin.resolve_blocks(self.reviews)

    def resolve_short_bio(self, info):
        if len(self.bio) > 80:
            return self.bio[:80] + ' ...'

        return self.bio


class ServiceNode(graphene.ObjectType):
    image = graphene.Field(ImageNode)

    more = graphene.List(
        ImageNode,
        start=graphene.Int(0),
        size=graphene.Int(30)
    )
    similar = graphene.List(ImageNode)
    operators = graphene.List(OperatorNode)

    def resolve_image(self, info):
        return self

    def resolve_similar(self, info):
        # FIXME for the moment this is as good as it gets
        # ordering after a search and keeping the relevance requires a custom scoring function
        # nothing special, but I don't know yet how to implement this in wagtail
        #
        # and in addition calling len(.) materializes the results which we don't like
        # because we want to keep the first 6 anyway
        #

        # FIXME since we do not have such data at the moment lets, ignore it
        # similar = get_image_model().objects.exclude(pk=self.pk).filter(rating__gt=1).search(self.all_tags_str)[:6]
        # if len(similar) < 6:
        #     similar = get_image_model().objects.exclude(pk=self.pk).search(self.all_tags_str)[:6]
        # return similar

        # results = get_image_model().objects.exclude(pk=self.pk) \
        #               .search(self.styles_str, fields=['styles_str'], operator='and') \
        #               .search(self.parts_str + self.minor_tags_str, operator='or')[:6]
        #
        # return results
        results = get_image_model().objects.exclude(pk=self.pk)
        if self.styles_tags:
            results = results.filter(styles_tags__contains=self.styles_tags).values_list('pk', flat=True)[:200]

        # This should work, but doesn't
        # results = get_image_model().objects.exclude(pk=self.pk).filter(styles_tags__contains=['Fineline']).search(self.all_tags_str)[:6]

        # unfortunately this is necessary because wagtail search
        # though a great search interface cannot handle ArrayFields
        # it can handle single values, but then the sql query to actually
        # get the data from the db gets screwed...
        #
        return SearchQuery.search(self.all_tags_str, filter_args={'pk__in': results})[:6]

    def resolve_operators(self, info):
        image_tags = self.tags.values_list('pk', flat=True)
        return OperatorPage.objects.live().filter(tags__pk__in=image_tags).distinct()

    @graphene.resolve_only_args
    def resolve_more(self, **kwargs):
        # FIXME: rethink matching on partial words
        # cause currently we match e.g. Portrait with Po

        start = kwargs.get('start')
        size = kwargs.get('size')

        return SearchQuery.search(self.all_tags_str, exclude_args={'pk': self.pk})[start:start + size]
