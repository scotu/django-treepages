from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from treepages.models import Page
from treepages.forms import PageAdminModelForm

from feincms.admin import editor

class PageAdmin(editor.TreeEditor):
    form = PageAdminModelForm
    # the fieldsets config here is used for the add_view, it has no effect
    # for the change_view which is completely customized anyway
    fieldsets = (
        (None,
            {
                'fields': ('active',
                           'in_navigation',
                           'template',
                           'title',
                           #'slug',
                           #'parent',
                           'body',)
            },
        ),
    )

    list_display = [
        #'short_title',
        'title',
        'cached_url_admin',
        'slug',
        'is_visible_admin',
        'in_navigation_toggle',
        'template']
    list_filter = ('active', 'in_navigation', 'template',)
    search_fields = ('title', 'slug', 'body',)
    #prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = []

    show_on_top = ('title', 'active')

    def changelist_view(self, *args, **kwargs):
        # get a list of all visible pages for use by is_visible_admin
        self._visible_pages = list(Page.objects.active().values_list('id', flat=True))

        return super(PageAdmin, self).changelist_view(*args, **kwargs)

    def is_visible_admin(self, page):
        if page.parent_id and not page.parent_id in self._visible_pages:
            # parent page's invisibility is inherited
            if page.id in self._visible_pages:
                self._visible_pages.remove(page.id)
                return u'%s (%s)' % (editor.django_boolean_icon(False), _('inherited'))

            return u'%s (%s)' % (editor.django_boolean_icon(False), _('not active'))

        if not page.id in self._visible_pages:
            return u'%s (%s)' % (editor.django_boolean_icon(False), _('not active'))

        return editor.django_boolean_icon(True)
    is_visible_admin.allow_tags = True
    is_visible_admin.short_description = _('is visible')

    def cached_url_admin(self, page):
        return u'<a href="%s">%s</a>' % (page._cached_url, page._cached_url)
    cached_url_admin.allow_tags = True
    cached_url_admin.admin_order_field = '_cached_url'
    cached_url_admin.short_description = _('Cached URL')

    in_navigation_toggle = editor.ajax_editable_boolean('in_navigation', _('in navigation'))
    
    def save_model(self, request, instance, form, change):
        instance.author = request.user
        super(PageAdmin, self).save_model(request, instance, form, change)

admin.site.register(Page, PageAdmin)
