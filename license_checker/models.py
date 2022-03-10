from django.db import models


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
    # sold_at = models.DateTimeField()
    # supported_until = models.DateTimeField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.license_code
