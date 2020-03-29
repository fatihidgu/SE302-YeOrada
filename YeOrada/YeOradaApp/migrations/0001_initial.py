# Generated by Django 3.0.4 on 2020-03-26 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=200, unique=True)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('isCustomer', models.BooleanField(default=False)),
                ('isClient', models.BooleanField(default=False)),
                ('isAdmin', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('userEmail',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('userEmail',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                   to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=300)),
                ('state', models.CharField(max_length=200)),
                ('workingHours', models.CharField(max_length=200)),
                ('workingDays', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('userEmail',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                   to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=300)),
                ('bio', models.CharField(max_length=200)),
            ],
        ),
    ]