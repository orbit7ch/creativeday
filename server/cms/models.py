from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from taggit.models import TaggedItemBase
from wagtail.core.models import Page as WagtailPage
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.images.models import AbstractImage, AbstractRendition
from django.contrib.postgres.fields import ArrayField, JSONField

from cms.blocks import RichTextBlock, ImageBlock, HeroBlock, HeroTextBlock, LogoBlock, TilesBlock, \
    ButtonBlock, SwiperBlock, CarouselBlock, MoreImagesBlock, IconBlock, PageContentBlock, \
    PlainImageBlock, ReviewBlock, AvatarTextBlock, FormBlock, SearchBlock, TextSearchBlock
from wagtail.search import index
from django.db import models

from cms.tagging import DELETE_IMAGE
from core.utils import overwrite_media_domain

CONTENT_BLOCK = [
    ('hero', HeroBlock(icon='pick')),
    ('herotext', HeroTextBlock(icon='pick')),
    ('text', RichTextBlock(icon='pilcrow')),
    ('button', ButtonBlock(icon='media')),
    ('swiper', SwiperBlock(icon='code')),
    ('carousel', CarouselBlock(icon='code')),
    ('tiles', TilesBlock(icon='grip')),
    ('image', ImageBlock(icon='picture')),
    ('logo', LogoBlock(icon='radio-full')),
    ('more', MoreImagesBlock(icon='plus-inverse')),
    ('icon', IconBlock(icon='picture')),
    ('form', FormBlock(icon='mail')),
    ('pagecontent', PageContentBlock(icon="placeholder")),
    ('avatar', AvatarTextBlock(icon="user")),
    ('search', SearchBlock(icon="search")),
    ('textsearch', TextSearchBlock(icon="search"))
]


class BasePage(WagtailPage):
    # does not work, sub class has to implement it
    # template = 'generic_page.html'
    class Meta:
        abstract = True

    menu_position = models.CharField(choices=[('main', 'Main Menu'), ('minor', 'Minor Menu')],
                                     max_length=255,
                                     default=None,
                                     blank=True,
                                     null=True)

    hide_for_search_engines = models.BooleanField(default=False)

    promote_panels = [
        FieldPanel('slug'),
        FieldPanel('seo_title'),
        FieldPanel('menu_position'),
        FieldPanel('hide_for_search_engines'),
    ]

    def get_sitemap_urls(self):
        if self.hide_for_search_engines:
            return []
        else:
            return super(BasePage, self).get_sitemap_urls()


class Page(BasePage):
    heading_alignment = models.CharField(
        choices=[
            ('left', 'Left'),
            ('center', 'Center')
        ],
        default='left',
        max_length=24
    )

    content_panels = WagtailPage.content_panels + [
        FieldPanel('heading_alignment'),
        StreamFieldPanel('content'),
    ]

    content = StreamField(CONTENT_BLOCK)
    template = 'generic_page.html'


class Operators(BasePage):
    parent_page_types = ['Page']
    subpage_types = ['cms.OperatorPage']
    template = 'generic_page.html'


class Companies(BasePage):
    parent_page_types = ['Page']
    subpage_types = ['cms.CompanyPage']
    template = 'generic_page.html'


class CompanyPage(BasePage):
    name = models.TextField()
    street = models.TextField()
    zip = models.TextField()
    city = models.TextField()
    bio = models.TextField(null=True, blank=True)

    latitude = models.DecimalField(max_digits=14, decimal_places=10)
    longitude = models.DecimalField(max_digits=14, decimal_places=10)

    portrait = StreamField([('image', PlainImageBlock(icon='picture')), ])

    content_panels = BasePage.content_panels + [
        StreamFieldPanel('portrait'),
        FieldPanel('name'),
        FieldPanel('bio'),
        FieldPanel('street'),
        FieldPanel('zip'),
        FieldPanel('city'),
        MultiFieldPanel(
            [
                FieldPanel('latitude'),
                FieldPanel('longitude'),
            ],
            heading="Coordinates (Use a tool like https://www.latlong.net/)",
        ),

    ]

    parent_page_types = ['Companies']
    subpage_types = []
    template = 'generic_page.html'


class OperatorPageTag(TaggedItemBase):
    content_object = ParentalKey('cms.OperatorPage', on_delete=models.CASCADE, related_name='tagged_items')


class OperatorPage(BasePage):
    pseudonym = models.TextField()
    full_name = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    tags = ClusterTaggableManager(through=OperatorPageTag, blank=True)

    portrait = StreamField([('image', PlainImageBlock(icon='picture')), ])
    portfolio = StreamField([('image', PlainImageBlock(icon='picture')), ], null=True, blank=True)

    companies = ParentalManyToManyField(CompanyPage, null=True, blank=True)

    reviews = StreamField([('review', ReviewBlock(icon='group')), ], null=True, blank=True)

    search_fields = Page.search_fields + [  # Inherit search_fields from Page
        index.SearchField('full_name'),
        index.SearchField('reviews'),
        index.RelatedFields('tags', [
            index.SearchField('name')
        ]),
    ]

    content_panels = BasePage.content_panels + [
        StreamFieldPanel('portrait'),
        FieldPanel('pseudonym'),
        FieldPanel('full_name'),
        FieldPanel('bio'),
        FieldPanel('tags'),
        StreamFieldPanel('portfolio'),
        FieldPanel('companies'),
        StreamFieldPanel('reviews'),
    ]

    parent_page_types = ['Operators']
    subpage_types = []
    template = 'generic_page.html'


class CmsImage(AbstractImage):
    rating = models.PositiveIntegerField(default=0, blank=True, null=True)

    # legacy
    all_tags_str = models.TextField(blank=True, null=True)

    # string copy of tags
    all_tags = ArrayField(models.CharField(max_length=100, blank=True), default=[])
    styles_tags = ArrayField(models.CharField(max_length=100, blank=True), default=[])
    parts_tags = ArrayField(models.CharField(max_length=100, blank=True), default=[])
    minor_tags = ArrayField(models.CharField(max_length=100, blank=True), default=[])

    url_200x200 = models.CharField(max_length=1024, blank=True, null=True)
    url_800x800 = models.CharField(max_length=1024, blank=True, null=True)
    url_400x400 = models.CharField(max_length=1024, blank=True, null=True)

    admin_form_fields = (
        'title',
        'file',
        'collection',
        'tags',
        'rating',
        # 'styles_tags', 'parts_tags', 'minor_tags'
    )

    search_fields = AbstractImage.search_fields + [
        index.SearchField('all_tags', partial_match=True),
        index.SearchField('styles_tags', partial_match=True, boost=10),
        index.SearchField('parts_tags', partial_match=True, boost=5),
        index.SearchField('minor_tags', partial_match=True),

        # index.AutocompleteField('all_tags'),
        # index.AutocompleteField('styles_tags'),

        index.SearchField('all_tags_str', partial_match=True),
        index.FilterField('id'),
        index.FilterField('rating'),
        index.FilterField('styles_tags'),
        index.FilterField('parts_tags'),
        index.FilterField('minor_tags')
    ]

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def make_semantic_tags(self):
        styles = []
        parts = []
        minor = []
        all_tags = []

        for tag in list(set(self.tags.all().values_list('name', flat=True))):
            all_tags.append(tag)

        self.styles_tags = styles
        self.parts_tags = parts
        self.minor_tags = minor
        self.all_tags = all_tags

        # legacy
        self.all_tags_str = ' '.join(all_tags)


class CmsRendition(AbstractRendition):
    image = models.ForeignKey(CmsImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


@receiver(post_save, sender=CmsImage)
def cms_image_post_save(sender, **kwargs):
    image = kwargs.get('instance')
    if image:
        save = False
        if not image.url_800x800:
            image.url_800x800 = overwrite_media_domain(image.get_rendition('max-800x800|format-jpeg').url)
            save = True

        if not image.url_200x200:
            image.url_200x200 = overwrite_media_domain(image.get_rendition('max-200x200|format-jpeg').url)
            save = True

        if not image.url_400x400:
            image.url_400x400 = overwrite_media_domain(image.get_rendition('max-400x400|format-jpeg').url)
            save = True

        if save:
            image.save()

        # wagtail admin interface
        image.get_rendition('max-165x165|format-jpeg')


@receiver(m2m_changed, sender=CmsImage.tags.through)
def cms_image_tags_changed(sender, **kwargs):
    image = kwargs.get('instance')
    if 'post_' in kwargs.get('action') and image.collection.name == 'services':
        image.make_semantic_tags()

        if image.all_tags_str:
            image.title = image.all_tags_str[:254]

        image.save()

    if image.tags.filter(name=DELETE_IMAGE).exists():
        image.delete()


class UserSearchTerm(TimeStampedModel):
    fields = JSONField()
    session_id = models.CharField(max_length=512, null=True, blank=True)
    ga_id = models.CharField(max_length=512, null=True, blank=True)
    is_internal = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)

    nbr_results = models.IntegerField(default=0)
    has_results = models.BooleanField(default=False)

    @property
    def fields_clean(self):
        try:
            return ', '.join(['%s: %s' % (k, v) for k, v in list(self.fields.items())])
        except:
            pass
        return ''
