from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from home.utils import get_top_tags, get_all_hub_peek_articles, get_hub_peek_articles

class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        'Content',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )
    
    
class HomePage(Page):
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        articles = Content.objects.live().order_by('-first_published_at')
        context['articles'] = articles
        context['tags'] = get_top_tags()
        context['hub_peeks'] = get_all_hub_peek_articles()
        return context

class Hub(Page):
    def get_context(self, request):
        context = super().get_context(request)
        tag = request.GET.get('tag')
        articles = Content.objects.filter(tags__name=tag).live().order_by('-first_published_at')
        context['articles'] = articles
        context['tags'] = get_top_tags()
        context['hub_peek'] = get_hub_peek_articles(tag)
        context['hub_page_title'] = tag
        return context
    
class Content(Page):
    date = models.DateField("Post date")
    article_title = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=ArticleTag, blank=True)
    search_fields = Page.search_fields + [
        index.SearchField('article_title'),
        index.SearchField('body'),
    ]
    

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('tags'),
        ], heading="Article Tags"),
        FieldPanel('date'),
        FieldPanel('article_title'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
        
    def get_context(self, request):
        context = super().get_context(request)
        context['tags'] = get_top_tags()
        return context

class ArticleGalleryImage(Orderable):
    page = ParentalKey(Content, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]