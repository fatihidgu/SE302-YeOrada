# Generated by Django 3.0.4 on 2020-04-15 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YeOradaApp', '0014_merge_20200410_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='customer_pics'),
        ),
    ]
