# Generated by Django 2.2.7 on 2019-12-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='img',
            field=models.ImageField(blank=True, default='http://placehold.it/380x500', null=True, upload_to='img/avatar'),
        ),
    ]
