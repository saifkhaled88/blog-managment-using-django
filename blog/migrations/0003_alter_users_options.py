# Generated by Django 5.1.2 on 2025-01-31 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_users_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'managed': False},
        ),
    ]
