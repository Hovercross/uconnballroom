from django.conf.urls import patterns, url

from dashboard.views import reporting, index, autocomplete, tracker

urlpatterns = patterns('',
    url(r'^$', index.index),
    url(r'^reports/$', reporting.index),
    url(r'^reports/report/$', reporting.report),
    url(r'^reports/person_info/$', reporting.person_info),
    url(r'^autocomplete/$', autocomplete.search),
    url(r'^tracker/$', tracker.index),
    url(r'^tracker/record/$', tracker.record_entry),
)
