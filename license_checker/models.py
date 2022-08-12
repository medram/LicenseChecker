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

    force = models.BooleanField(_('Force Override!'), default=False,
                                blank=True, help_text=_('Override Envato license info (license type, status & amount), required for custom licenses!'))

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    @classmethod
    def get_license(cls, license_code):
        try:
            return cls.objects.get(license_code=license_code)
        except cls.DoesNotExist:
            return None

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

        if valid:
            valid = False if self.envato_app_id != str(
                data['item']['id']) else valid

        return data, valid

    def is_valid_license(self, license, valid):
        if (valid or license.force) and license.status == License.STATUS.ACTIVE:
            return True
        return False

    def update_license(self, license, data, valid=False):
        if license.app == self:
            if not license.force:
                license_type = License.TYPES.REGULAR_LICENSE if str(data.get(
                    'license')).lower() == 'regular license' else License.TYPES.EXTENDED_LICENSE

                license.status = License.STATUS.ACTIVE if valid else License.STATUS.INACTIVE
                license.license_type = license_type if valid else License.TYPES.REGULAR_LICENSE
                license.amount = float(data.get('amount', 0))

            license.save()

    def __str__(self):
        return self.app_name
