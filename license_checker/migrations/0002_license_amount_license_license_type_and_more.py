# Generated by Django 4.0.3 on 2022-03-10 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license_checker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='license',
            name='license_type',
            field=models.IntegerField(choices=[(0, 'Regular License'), (1, 'Extended License')], default=0),
        ),
        migrations.AlterField(
            model_name='license',
            name='status',
            field=models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive'), (2, 'Banned')], default=0),
        ),
    ]
