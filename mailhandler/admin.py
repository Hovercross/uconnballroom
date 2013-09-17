from django.contrib import admin

from django import forms

from django.utils.translation import ugettext_lazy as _

from mailhandler.models import MailSender

from django.template.defaultfilters import slugify
from django_ses.views import dashboard

class MailSenderAdmin(admin.ModelAdmin):
	pass

admin.site.register(MailSender, MailSenderAdmin)
