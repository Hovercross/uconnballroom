from django.conf.urls import patterns, url

from . import views

urlpatterns = [
    url(r'^gallery-manager/(\d+)/$', views.manage_gallery),
]