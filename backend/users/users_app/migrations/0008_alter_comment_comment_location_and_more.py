# Generated by Django 4.0.3 on 2022-09-15 23:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0007_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comment_location', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='commenters', to=settings.AUTH_USER_MODEL),
        ),
    ]
