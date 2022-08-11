from django.contrib import admin
from .models import License, Domain, App


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('license_code', 'status', 'license_type',
                    'checks', 'amount', 'domains', 'updated', 'created')
    search_fields = ('license_code',)
    list_filter = ('status', 'license_type',
                   'app__app_name', 'created', 'updated')
    readonly_fields = ('checks',)
    autocomplete_fields = ('app',)

    @admin.display
    def domains(self, obj):
        return obj.domains.count()


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('host', 'checks', 'updated', 'created')
    search_fields = ('host', 'license__license_code')
    list_filter = ('created', 'updated')
    autocomplete_fields = ('license',)


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'envato_app_id', 'api_key', 'earnings', 'licenses',
                    'domains', 'checks', 'created')
    fields = ('app_name', 'envato_app_id')
    search_fields = ('app_name', 'api_key')
    list_filter = ('created',)

    @admin.display
    def licenses(self, obj):
        return obj.licenses.count()

    @admin.display
    def domains(self, obj):
        return sum(n for n in (license.domains.count() for license in obj.licenses.all()))

    @admin.display(description='Total checks')
    def checks(self, obj):
        return sum(license.checks for license in obj.licenses.all())

    @admin.display(description='earnings')
    def earnings(self, obj=None):
        return "$%.2f" % sum(license.amount for license in obj.licenses.all())
