# Generated by Django 5.1.3 on 2024-12-09 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
