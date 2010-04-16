from django.db import models
from django.db.models import Q, signals
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

import mptt
from autoslug.fields import AutoSlugField
from treepages.fields import ColorField
from django_extensions.db.models import TimeStampedModel

class PageManager(models.Manager):

    # A list of filters which are used to determine whether a page is active or not.
    # Extended for example in the datepublisher extension (date-based publishing and
    # un-publishing of pages)
    active_filters = [
        Q(active=True),
        ]

    @classmethod
    def apply_active_filters(cls, queryset):
        for filt in cls.active_filters:
            if callable(filt):
                queryset = filt(queryset)
            else:
                queryset = queryset.filter(filt)

        return queryset

    def active(self):
        return self.apply_active_filters(self)

    def page_for_path(self, path, raise404=False):
        """
        Return a page for a path.

        Example:
        Page.objects.page_for_path(request.path)
        """

        stripped = path.strip('/')

        try:
            return self.active().get(_cached_url=stripped and u'/%s/' % stripped or '/')
        except self.model.DoesNotExist:
            if raise404:
                raise Http404
            raise

    def page_for_path_or_404(self, path):
        """
        Wrapper for page_for_path which raises a Http404 if no page
        has been found for the path.
        """
        return self.page_for_path(path, raise404=True)

    def in_navigation(self):
        return self.active().filter(in_navigation=True)

    def toplevel_navigation(self):
        return self.in_navigation().filter(parent__isnull=True)



class Page(TimeStampedModel):
    active = models.BooleanField(_('active'), default=False)

    # properties
    author = models.ForeignKey(User, related_name='created_pages')
    title = models.CharField(_('title'), max_length=100,
        help_text=_('This is used for the generated navigation too.'))
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    body = models.TextField(_('body'))
    associated_color = ColorField(_('associated color'), blank=True, default='')
    # structure and navigation
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    in_navigation = models.BooleanField(_('in navigation'), default=True)
    _cached_url = models.CharField(_('cached URL'), max_length=200, blank=True,
        editable=False, default='', db_index=True)

    class Meta:
        ordering = ['tree_id', 'lft']
        verbose_name = _('page')
        verbose_name_plural = _('pages')

    objects = PageManager()

    def __unicode__(self):
        return u'%s' % self.title

    def get_RGB_color(self):
        return self.associated_color[:6]

    def are_ancestors_active(self):
        """
        Check whether all ancestors of this page are active
        """

        if self.is_root_node():
            return True

        queryset = PageManager.apply_active_filters(self.get_ancestors())
        return queryset.count() >= self.level


    def save(self, *args, **kwargs):
        cached_page_urls = {}

        
        # salvo in modo che lo slug sia creato da AutoSlugField
        super(Page, self).save(*args, **kwargs)

        # determine own URL
        if self.is_root_node():
            self._cached_url = u'/%s/' % self.slug
        else:
            self._cached_url = u'%s%s/' % (self.parent._cached_url, self.slug)
        cached_page_urls[self.id] = self._cached_url
        super(Page, self).save(*args, **kwargs)

        # make sure that we get the descendants back after their parents
        pages = self.get_descendants().order_by('lft')
        for page in pages:
            # cannot be root node by definition
            page._cached_url = u'%s%s/' % (
                cached_page_urls[page.parent_id],
                page.slug)

            cached_page_urls[page.id] = page._cached_url
            super(Page, page).save() # do not recurse

    def get_absolute_url(self):
        return self._cached_url

    def get_preview_url(self):
        # to have previews add this url:
        # url(r'^preview/(?P<page_id>\d+)/', base.preview_handler, name='treepages_preview'),
        try:
            return reverse('treepages_preview', kwargs={ 'page_id': self.id })
        except:
            return None

mptt.register(Page)
