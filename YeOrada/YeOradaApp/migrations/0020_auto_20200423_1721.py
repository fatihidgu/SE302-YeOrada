# Generated by Django 3.0.4 on 2020-04-23 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YeOradaApp', '0019_auto_20200417_0254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='country',
            new_name='state',
        ),
    ]
