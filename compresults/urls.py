from django.conf.urls import patterns, url

import compresults.views

urlpatterns = [
    url(r'^projector/$', compresults.views.projector),
    url(r'^json/projector/$', compresults.views.projector_json, name='json-projector'),
]