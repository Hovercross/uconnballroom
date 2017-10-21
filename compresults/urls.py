from django.conf.urls import patterns, url
from django.views.generic import TemplateView

import compresults.views

urlpatterns = [
    url(r'^projector/$', TemplateView.as_view(template_name="compresults/projector.html")),
    url(r'^$', TemplateView.as_view(template_name="compresults/web.html")),
    url(r'^json/$', compresults.views.json, name='json'),
]