from django.conf.urls import patterns, url

import lists.views

urlpatterns = patterns('',
    url(r'^remote/scan/process/(?P<id>[0-9]+)/$', lists.views.remoteScan),
    url(r'^remote/scan/setup/(?P<id>[0-9]+)/$', lists.views.remoteScanSetup, name='lists_remotescan_setup'),
)
