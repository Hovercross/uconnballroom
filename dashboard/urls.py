from django.conf.urls import patterns, url

import dashboard.views

urlpatterns = patterns('',
    url(r'^$', dashboard.views.index),
    url(r'^reports/', dashboard.views.reporting),
    url(r'^autocomplete/', dashboard.views.autocomplete),
    url(r'^entry_tracker/record/', dashboard.views.record_entry),
)
