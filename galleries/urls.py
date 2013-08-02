from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^gallery-manager/(\d+)/$', views.manage_gallery),
)