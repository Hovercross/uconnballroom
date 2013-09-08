from django.conf.urls import patterns, url

import registration.views.frontend

urlpatterns = patterns('',
    url(r'^$', registration.views.frontend.index),
)
