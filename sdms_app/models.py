from django.db import models

# subpage_types = []
# parent_page_types = ['mysite.modelname']

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
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TagBase, ItemBase

# https://tentacles666.wordpress.com/2011/10/29/django-hierarchical-tags-with-taggit-and-tree/comment-page-1/
# title will be name , intro will be about student ,   
class StudentList(Page):
    intro = RichTextField(blank=True)
    parent_page_types = [] 
    subpage_types = ['sdms_app.Student']
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ] 
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['studentslist'] = blogpages
        # # Filter by tag
        # tag = request.GET.get('tag')
        # if tag:
        #     blogpages = blogpages.filter(tags__name=tag)

        # context['studentslist'] = blogpages
        return context

  


# https://docs.wagtail.io/en/v2.10.1/reference/pages/model_recipes.html#disabling-free-tagging


# @register_snippet
# class StudentTag(TagBase):
    
#     free_tagging = False
#     content_object = ParentalKey(
#         'Student',
#         related_name='tagged_items',
#         on_delete=models.SET("CorrespondingStudentDeleted")
#     )
#     class Meta:
#         verbose_name = "blog tag"
#         verbose_name_plural = "blog tags"

# class StudentTag(TaggedItemBase):
#     content_object = ParentalKey('sdms_app.Student', on_delete=models.SET("CorrespondingStudentDeleted"), related_name='tagged_items')
# @register_snippet
# class StudentTag(TagBase):

class StudentTag(TaggedItemBase):

    free_tagging = True
    class Meta:
        verbose_name = "blog tag"
        verbose_name_plural = "blog tags"

class TaggedStudent(ItemBase):
    tag = models.ForeignKey(
        StudentTag, related_name="tagged_blogs", on_delete=models.SET('TagDeleted')
    )
    content_object = ParentalKey(
        to='sdms_app.Student',
        on_delete=models.SET('StudentDeleted'),
        related_name='tagged_items' )

# https://docs.wagtail.io/en/v2.10.1/reference/pages/model_reference.html#page
#  owner gives info about who is owner of this page

class FeeSubmited():
    amount = models.IntegerField(max_length=6)
    # submitted_on = models.


class Student(Page):
    date = models.DateField("Admission date")

  
    intro = models.CharField(max_length=250,blank=True)
    #  = models.CharField(max_length=250,blank=True)
    body = RichTextField(blank=True)
    # tags = ClusterTaggableManager(through=StudentTag, blank=True)
    tags = ClusterTaggableManager(through='sdms_app.TaggedStudent', blank=True)

    # tags = ClusterTaggableManager(through=StudentTag, blank=True)
    parent_page_types = ['sdms_app.StudentList']
    
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
            FieldPanel('intro'),
            FieldPanel('tags'),
        ], heading="Tags associated with student"),
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
        InlinePanel('submitted_fees', label="fees info"),
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


class FeesInfo(Orderable):
    page = ParentalKey(Student, blank=True, null=True, on_delete=models.CASCADE, related_name='submitted_fees')
    entry_by= models.CharField(blank= False ,max_length=250)
    fee_submitted = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('entry_by'),
        FieldPanel('fee_submitted'),
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