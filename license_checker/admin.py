from django.contrib import admin
from .models import License, Domain, App


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('license_code', 'status', 'license_type',
                    'checks', 'amount', 'updated', 'created')
    search_fields = ('license_code',)
    list_filter = ('status', 'license_type', 'app__app_name', 'created', 'updated')
    readonly_fields = ('checks',)
    autocomplete_fields = ('app',)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('host', 'checks', 'updated', 'created')
    search_fields = ('host', 'license__license_code')
    list_filter = ('created', 'updated')
    autocomplete_fields = ('license',)


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'api_key', 'created')
    fields = ('app_name', 'api_key')
    search_fields = ('app_name', 'api_key')
    list_filter = ('created',)
