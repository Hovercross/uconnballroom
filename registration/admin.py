from django.contrib import admin

from django import forms

from adminsortable.admin import SortableTabularInline, SortableAdmin
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ObjectDoesNotExist

from models import PersonType, RegistrationSession, List, PersonEmail, Person, Registration, PersonTypeAutoList, QueryList
from django.template.defaultfilters import slugify
from django_ses.views import dashboard

class AutoListPersonTypeInlineAdmin(admin.TabularInline):
	model = PersonTypeAutoList
	

class QueryListAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name', )}
	fields = ['name', 'slug',  'query_string', 'unrestricted_send', 'showPeople']
	readonly_fields = ('showPeople', )
	
	def showPeople(self, o):
		try:
			people = list(o.people)
		except Exception, e:
			return "Error parsing query list"
			
		people.sort(key=lambda x: (x.last_name, x.first_name))
		
		print people
		
		return ", ".join(map(str, people))
	
	showPeople.short_description = "People"	
	showPeople.allow_tags = True
class PersonTypeAdmin(SortableAdmin):
	inlines = [AutoListPersonTypeInlineAdmin]

class ListAdmin(admin.ModelAdmin):
	filter_horizontal = ('included_lists', 'included_people')

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

	def save_model(self, request, obj, form, change):
		#Take care of list creation
		auto_names = (
			('club_paid_list', 'club', '-paid'),
			('club_unpaid_list', 'club', '-unpaid'),
			('team_paid_list', 'team', '-paid'),
			('team_unpaid_list', 'team', '-unpaid'),
		)
		
		for attr, autoPrefix, autoSuffix in auto_names:
			try:
				related_list = getattr(obj, attr)
			except ObjectDoesNotExist, e:
				related_list = None
			
			if not related_list:
				auto_list_name = "%s%s%s" % (autoPrefix, obj.card_code.lower(), autoSuffix)
				try:
					l = List.objects.get(name=auto_list_name)
				except ObjectDoesNotExist, e:
					l = List(name=auto_list_name, slug=slugify(auto_list_name))
					l.internally_managed = True
					l.save()

				setattr(obj, attr, l)
				
		obj.save()

admin.site.register(RegistrationSession, RegistrationSessionAdmin)
admin.site.register(PersonType, PersonTypeAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(QueryList, QueryListAdmin)
