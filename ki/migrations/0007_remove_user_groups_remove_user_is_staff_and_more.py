# Generated by Django 4.2.1 on 2023-10-16 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ki', '0006_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
    ]
