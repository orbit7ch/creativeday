from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

DEFAULT_RICH_TEXT_FEATURES = ['h1', 'h2', 'h3', 'bold', 'italic', 'link', 'ul']


class BaseBlock(blocks.StructBlock):
    space_after = blocks.ChoiceBlock(choices=[
        ('pb-0', 'None'),
        ('pb-2', 'Small'),
        ('pb-4', 'Medium'),
        ('pb-5', 'Large')
    ], default='pb-4')


class HeroBlock(BaseBlock):
    background_image = ImageChooserBlock()
    text = blocks.TextBlock(required=False)
    button_page = blocks.PageChooserBlock(required=False)
    button_text = blocks.TextBlock(required=False)
    use_img_overlay = blocks.BooleanBlock(default=True, required=False)
    show_logo = blocks.BooleanBlock(default=True, required=False)

    slides_interval = blocks.IntegerBlock(default=0,
                                          help_text="The duration between slide cycles (in milliseconds, use 0 for no transition)")
    slides = blocks.ListBlock(
        blocks.StructBlock([
            ('image', DocumentChooserBlock()),
            ('text', blocks.TextBlock(required=False)),
        ], label="slides"),
        required=False
    )


class _FilterItem(blocks.StructBlock):
    image = ImageChooserBlock()
    text = blocks.CharBlock(required=False)


class SearchBlock(BaseBlock):
    use_endless_scrolling = blocks.BooleanBlock(default=True, required=False)
    show_text_search = blocks.BooleanBlock(default=True, required=False)
    initial_search = blocks.TextBlock(required=False)

    tags = blocks.ListBlock(
        blocks.TextBlock()
    )

    filters = blocks.ListBlock(_FilterItem)


class TextSearchBlock(BaseBlock):
    page = blocks.PageChooserBlock(required=False)


class HeroTextBlock(BaseBlock):
    background_image = ImageChooserBlock()
    text = blocks.RichTextBlock(features=DEFAULT_RICH_TEXT_FEATURES, required=False)
    button_link = blocks.PageChooserBlock(required=False)
    button_text = blocks.TextBlock(required=False)
    use_img_overlay = blocks.BooleanBlock(default=True, required=False)


class LogoBlock(BaseBlock):
    text = blocks.RichTextBlock(features=DEFAULT_RICH_TEXT_FEATURES, required=False)
    style = blocks.ChoiceBlock(choices=[
        ('light', 'Light'),
        ('dark', 'Dark')
    ], default='light')


class _ServiceItem(blocks.StructBlock):
    image = ImageChooserBlock()
    label = blocks.CharBlock(required=False)
    page = blocks.PageChooserBlock(required=False)
    searchText = blocks.CharBlock(required=False)


class TilesBlock(BaseBlock):
    heading = blocks.CharBlock(required=False)
    images = blocks.ListBlock(_ServiceItem)


class CarouselBlock(TilesBlock):
    pass


class SwiperBlock(TilesBlock):
    pass


class MoreImagesBlock(BaseBlock):
    pass


class ButtonBlock(BaseBlock):
    text = blocks.TextBlock(required=True)
    page = blocks.PageChooserBlock(required=False)
    search_text = blocks.CharBlock(required=False)


class PageContentBlock(BaseBlock):
    page = blocks.PageChooserBlock(required=False)


class RichTextBlock(BaseBlock):
    text = blocks.RichTextBlock(features=DEFAULT_RICH_TEXT_FEATURES)


class ImageBlock(BaseBlock):
    image = ImageChooserBlock()


class IconBlock(BaseBlock):
    document = DocumentChooserBlock()


class DocumentBlock(BaseBlock):
    document = DocumentChooserBlock()


class AvatarTextBlock(BaseBlock):
    image = ImageChooserBlock()
    heading = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ul'])


class PlainImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()


class ReviewBlock(blocks.StructBlock):
    name = blocks.TextBlock(required=False)
    text = blocks.TextBlock(required=False)
    rating = blocks.IntegerBlock(required=False)


class FormBlock(BaseBlock):
    form_name = blocks.CharBlock(required=True)
    confirmation_message = blocks.TextBlock(required=True, default="Danke für deine Anfrage")
    show_name = blocks.BooleanBlock(default=True, required=False)
    show_email = blocks.BooleanBlock(default=True, required=False)
    show_phone = blocks.BooleanBlock(default=True, required=False)
    show_message = blocks.BooleanBlock(default=True, required=False)
