# Generated by Django 3.2.8 on 2021-11-02 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0004_auto_20211102_0132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='birthday',
            new_name='birth_date',
        ),
    ]
