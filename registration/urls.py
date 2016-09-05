from django.conf.urls import patterns, url, include
from rest_framework import routers

import registration.views.frontend
import registration.views.admin
import registration.views.api

router = routers.DefaultRouter()
router.register('people', registration.views.api.PersonViewSet)

urlpatterns = [
    url(r'^$', registration.views.frontend.index),
    url(r'^payment/$', registration.views.admin.payment),
    url(r'^api/', include(router.urls))
]