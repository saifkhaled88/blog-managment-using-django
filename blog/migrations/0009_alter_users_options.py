# Generated by Django 5.1.2 on 2025-02-02 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_users_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'managed': True},
        ),
    ]
