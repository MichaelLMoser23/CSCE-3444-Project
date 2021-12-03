# Generated by Django 3.2.8 on 2021-11-24 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialmedia', '0016_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blocked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blocked_users', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, related_name='blocked_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]