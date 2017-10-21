from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

import django.contrib.auth.views

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^accounts/login/', django.contrib.auth.views.login, {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout), 
    url(r'^mail/', include('mailhandler.urls')),
    url(r'^lists/', include('lists.urls')),
    url(r'^compresults/', include('compresults.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', include('galleries.urls')),
    url(r'', include('feincms.urls')),
]

if settings.SERVE_STATIC:
	urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)