from django.contrib import admin

from django import forms

from adminsortable.admin import SortableTabularInline, SortableAdmin
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ObjectDoesNotExist

from models import PersonType, RegistrationSession, List, PersonEmail, Person, Registration
from django.template.defaultfilters import slugify
from django_ses.views import dashboard

class PersonTypeAdmin(SortableAdmin):
	pass

class ListAdmin(admin.ModelAdmin):
	pass

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
	fields = ['person_type', 'team', 'amount_due', 'sent_registration_email']
	ordering = ('registration_session__year', '-registration_session__semester')
	
	readonly_fields = ('amount_due', )
	

class PersonAdmin(admin.ModelAdmin):
	inlines = [InlineEmailAdmin, InlineRegistrationAdmin]
	search_fields = ['first_name', 'last_name']
	
class RegistrationSessionAdmin(admin.ModelAdmin):
	fields = ['year', 'semester', 'card_code', 'base_price', 'team_surcharge', 'nonstudent_surcharge', 'returning_discount', 'early_discount', 'early_deadline', 'first_club_day', 'last_free_day', 'available']
	
	list_display = ['year', 'semester', 'available']
	
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
					l.save()

				setattr(obj, attr, l)
				
		obj.save()

admin.site.register(RegistrationSession, RegistrationSessionAdmin)
admin.site.register(PersonType, PersonTypeAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Person, PersonAdmin)
