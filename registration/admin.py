from django.contrib import admin

from django import forms

from adminsortable.admin import SortableTabularInline, SortableAdmin
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ObjectDoesNotExist

from models import PersonType, RegistrationSession, PersonEmail, Person, Registration, PersonTypeAutoList
from django.template.defaultfilters import slugify

class AutoListPersonTypeInlineAdmin(admin.TabularInline):
	model = PersonTypeAutoList
	


class PersonTypeAdmin(SortableAdmin):
	inlines = [AutoListPersonTypeInlineAdmin]


class EmailAdminForm(forms.ModelForm):
	class Meta:
		model = PersonEmail
		
	def clean_email(self):
		return self.cleaned_data["email"].lower()

class InlineEmailAdmin(admin.TabularInline):
	model = PersonEmail
	form = EmailAdminForm
	
class InlineRegistrationAdmin(admin.TabularInline):
	model = Registration
	fields = ['person_type', 'team', 'registered_at', 'amount_due', 'paid_amount', 'sent_registration_email']
	ordering = ('registration_session__year', '-registration_session__semester')
	
	readonly_fields = ('amount_due', 'registered_at', 'paid_amount')

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

class PersonAdmin(admin.ModelAdmin):
	inlines = [InlineEmailAdmin, InlineRegistrationAdmin]
	search_fields = ['first_name', 'last_name']
	
	def has_delete_permission(self, request, obj=None):
		if not request.user.has_perm('registration.delete_person'):
			return False

		if not obj:
			return request.user.has_perm('registration.delete_person')

		for r in obj.registration_set.all():
			if r.paid_amount > 0:
				return False

		return request.user.has_perm('registration.delete_person')

class RegistrationSessionAdmin(admin.ModelAdmin):
	fields = ['year', 'semester', 'card_code', 'base_price', 'team_surcharge', 'nonstudent_surcharge', 'returning_discount', 'early_discount', 'early_deadline', 'first_club_day', 'last_free_day', 'available']
	
	list_display = ['year', 'semester', 'available']

	inlines = [InlineRegistrationAdmin]

	def has_delete_permission(self, request, obj=None):
		if not request.user.has_perm('registration.delete_registrationsession'):
			return False

		if not obj:
			return request.user.has_perm('registration.delete_registrationsession')
	
		if obj.registration_set.count() > 0:
			return False

		return request.user.has_perm('registration.delete_registrationsession')

admin.site.register(RegistrationSession, RegistrationSessionAdmin)
admin.site.register(PersonType, PersonTypeAdmin)
admin.site.register(Person, PersonAdmin)
