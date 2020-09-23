from django.db import models

# Create your models here.

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from taggit.models import TagBase
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

# title will be name , intro will be about student ,   
class StudentList(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['studentslist'] = blogpages
        return context


# https://docs.wagtail.io/en/v2.10.1/reference/pages/model_recipes.html#disabling-free-tagging


@register_snippet
class StudentTag(TagBase):
    
    free_tagging = False
    content_object = ParentalKey(
        'Student',
        related_name='tagged_items',
        on_delete=models.SET("CorrespondingStudentDeleted")
    )
    class Meta:
        verbose_name = "blog tag"
        verbose_name_plural = "blog tags"




# https://docs.wagtail.io/en/v2.10.1/reference/pages/model_reference.html#page
#  owner gives info about who is owner of this page
class Student(Page):
    date = models.DateField("Admission date")

  
    intro = models.CharField(max_length=250,blank=True)
    body = RichTextField(blank=True)

    tags = ClusterTaggableManager(through=StudentTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            # FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Tags associated with student"),
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(Student, on_delete=models.SET("CorrespondingStudentDeleted"), related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET("ImageDeletedFromGallery"), related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]




# class BlogPageTag(TaggedItemBase):
#     content_object = ParentalKey(
#         'Student',
#         related_name='tagged_items',
#         on_delete=models.CASCADE
#     )

class StudentTagIndex(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context