from django.contrib import admin

from costumes.models import Costume, Maintenance

class MaintenanceInline(admin.TabularInline):
    model = Maintenance
    extra = 0

class CostumeAdmin(admin.ModelAdmin):
    inlines = [MaintenanceInline]

class MaintenanceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Costume, CostumeAdmin)    
admin.site.register(Maintenance, MaintenanceAdmin)
