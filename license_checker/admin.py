from django.contrib import admin
from .models import License, Domain


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('license_code', 'status', 'license_type',
                    'checks', 'amount', 'updated', 'created')
    search_fields = ('license_code',)
    list_filter = ('status', 'license_type', 'created', 'updated')
    readonly_fields = ('checks',)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('host', 'checks', 'updated', 'created')
    search_fields = ('host', 'license__license_code')
    list_filter = ('created', 'updated')
    autocomplete_fields = ('license',)
