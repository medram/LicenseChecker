import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from .common import generate_api_key, verify_envato_license_code

ENVATO_TOKEN = os.getenv('ENVATO_TOKEN', None)


class License(models.Model):
    class STATUS(models.IntegerChoices):
        ACTIVE = (0, 'Active')
        INACTIVE = (1, 'Inactive')
        BANNED = (2, 'Banned')

    class TYPES(models.IntegerChoices):
        REGULAR_LICENSE = (0, 'Regular License')
        EXTENDED_LICENSE = (1, 'Extended License')

    license_code = models.CharField(max_length=256)
    license_type = models.IntegerField(
        choices=TYPES.choices, default=TYPES.REGULAR_LICENSE)
    status = models.IntegerField(choices=STATUS.choices, default=STATUS.ACTIVE)
    checks = models.IntegerField(default=0, blank=True)

    amount = models.FloatField(default=0)
    app = models.ForeignKey(
        'App', on_delete=models.CASCADE, related_name='licenses')
    # sold_at = models.DateTimeField()
    # supported_until = models.DateTimeField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.license_code


class Domain(models.Model):
    license = models.ForeignKey(
        'License', on_delete=models.CASCADE, related_name='domains')
    host = models.CharField(max_length=64)
    checks = models.IntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.host


class App(models.Model):
    api_key = models.CharField(max_length=256, default=generate_api_key)
    app_name = models.CharField(max_length=40)
    envato_app_id = models.CharField(_('Envato App ID'), max_length=40)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def verify_envato_license_code(self, code):
        data, valid = verify_envato_license_code(code, ENVATO_TOKEN)
        valid = False if self.envato_app_id != str(
            data['item']['id']) else valid

        print(valid)
        print(data)

        return data, valid

    def __str__(self):
        return self.app_name
