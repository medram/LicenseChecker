# Generated by Django 4.0.3 on 2022-03-11 08:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('license_checker', '0003_alter_license_options_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='domain',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
