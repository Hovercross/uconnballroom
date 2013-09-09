from django.conf.urls import patterns, url

import registration.views.frontend
import registration.views.admin

urlpatterns = patterns('',
    url(r'^$', registration.views.frontend.index),
    url(r'^payment/$', registration.views.admin.payment)
)
