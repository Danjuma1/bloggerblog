# Generated by Django 2.0.3 on 2018-04-13 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rammyblog', '0002_auto_20180413_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='Facebook_url',
            new_name='facebook_url',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='Google',
            new_name='google',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='Twitter_url',
            new_name='twitter_url',
        ),
    ]
