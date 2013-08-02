from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^bulk-uploader/(\d+)/$', views.manage_gallery),
)