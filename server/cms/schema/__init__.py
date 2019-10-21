import graphene
from django.shortcuts import get_object_or_404
from graphene_django.filter import DjangoFilterConnectionField
from taggit.models import Tag
from wagtail.images import get_image_model
from cms.models import Page, OperatorPage, CompanyPage, Operators, Companies
from cms.schema.wagtail import TagNode, ImageNode, DocumentNode, ImageFilter
from cms.schema.mutations import UpdateImage, StoreUserSearchTerm
from cms.schema.nodes import PageNode, OperatorNode, CompanyNode, ServiceNode
from cms.tagging import HIDE_FROM_SEARCH
from core.middleware import get_current_user
from graphene.types.generic import GenericScalar

from search.query import SearchQuery


class CmsQuery(graphene.ObjectType):
    service = graphene.Field(ServiceNode, pk=graphene.String())

    page = graphene.Field(PageNode, slug=graphene.String())
    pages = DjangoFilterConnectionField(PageNode)

    operator = graphene.Field(OperatorNode, slug=graphene.String())
    operators = graphene.List(OperatorNode)

    company = graphene.Field(CompanyNode, slug=graphene.String())
    companies = graphene.List(CompanyNode)

    menu = GenericScalar()

    # fulltext search endpoint
    service_search = graphene.List(
        ServiceNode,
        search_text=graphene.String(),
        start=graphene.Int(0),
        size=graphene.Int(30)
    )

    suggest = graphene.String(
        search_text=graphene.String()
    )

    # admin stuff
    tags = graphene.List(TagNode)
    images = DjangoFilterConnectionField(ImageNode, filterset_class=ImageFilter)

    @graphene.resolve_only_args
    def resolve_operator(self, **kwargs):
        slug = kwargs.get('slug')
        return OperatorPage.objects.live().get(slug=slug) if slug else None

    @graphene.resolve_only_args
    def resolve_operators(self, **kwargs):
        return OperatorPage.objects.live()

    @graphene.resolve_only_args
    def resolve_service(self, **kwargs):
        pk = kwargs.get('pk')
        return get_image_model().objects.get(pk=pk)

    @graphene.resolve_only_args
    def resolve_service_search(self, **kwargs):
        search_text = kwargs.get('search_text').lower()
        start = kwargs.get('start')
        size = kwargs.get('size')

        searched = SearchQuery.search(search_text)
        return searched[start:start + size]

    @graphene.resolve_only_args
    def resolve_suggest(self, **kwargs):
        return SearchQuery.suggestions(kwargs.get('search_text'))

    @graphene.resolve_only_args
    def resolve_company(self, **kwargs):
        slug = kwargs.get('slug')
        return CompanyPage.objects.live().get(slug=slug) if slug else None

    @graphene.resolve_only_args
    def resolve_companies(self, **kwargs):
        return CompanyPage.objects.live()

    @graphene.resolve_only_args
    def resolve_page(self, **kwargs):
        slug = kwargs.get('slug')

        if not slug:
            slug = 'homepage'

        return get_object_or_404(Page, slug=slug)

    @graphene.resolve_only_args
    def resolve_pages(self, *args):
        return Page.objects.live()

    # admin stuff ...
    @graphene.resolve_only_args
    def resolve_tags(self):
        u = get_current_user()
        if not u.is_superuser:
            return Tag.objects.none()

        return Tag.objects.all()

    @graphene.resolve_only_args
    def resolve_images(*args, **kwargs):
        # FIXME tagging app?
        u = get_current_user()
        if not u.is_superuser:
            return get_image_model().objects.none()

        return get_image_model().objects.filter(tags=None, collection__name='services').exclude(
            tags__name=HIDE_FROM_SEARCH).order_by('-id')

    @graphene.resolve_only_args
    def resolve_menu(self, *args):
        menu = {
            'main': [],
            'minor': []
        }

        for klass in [Page, Operators, Companies]:
            for p in klass.objects.filter(live=True, menu_position__isnull=False).values(
                    'title', 'seo_title', 'slug', 'menu_position'):
                menu[p['menu_position']].append({'title': p['seo_title'] or p['title'], 'url': '/{}'.format(p['slug'])})

        return menu


class CmsMutation(graphene.ObjectType):
    update_image = UpdateImage.Field()
    store_user_search_term = StoreUserSearchTerm.Field()
