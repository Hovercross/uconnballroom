from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from filebrowser.sites import site

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ballroomcms.views.home', name='home'),
    # url(r'^ballroomcms/', include('ballroomcms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('feincms.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)