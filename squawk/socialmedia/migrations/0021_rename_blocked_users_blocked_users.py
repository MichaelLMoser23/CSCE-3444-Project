# Generated by Django 3.2.8 on 2021-12-07 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0020_auto_20211206_2127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blocked',
            old_name='blocked_users',
            new_name='users',
        ),
    ]
