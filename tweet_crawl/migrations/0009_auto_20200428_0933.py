# Generated by Django 3.0.5 on 2020-04-28 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweet_crawl', '0008_auto_20200428_0931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='tweet_id',
            new_name='tweet',
        ),
    ]