from wagtail.core import hooks
from wagtail.contrib.redirects.models import Redirect

# Create redirect when editing slugs
@hooks.register('before_edit_page')
def create_redirect_on_slug_change(request, page):
    if request.method == 'POST':
        if page.slug != request.POST['slug']:
            Redirect.objects.create(
                    old_path=page.url[:-1],
                    site=page.get_site(),
                    redirect_page=page
                )