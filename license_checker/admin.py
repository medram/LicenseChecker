from django.contrib import admin
from .models import License


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('license_code', 'status', 'license_type',
                    'checks', 'amount', 'updated', 'created')
    search_fields = ('license_code',)
    list_filter = ('status', 'license_type', 'created', 'updated')
    readonly_fields = ('checks',)
