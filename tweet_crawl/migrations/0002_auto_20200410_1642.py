# Generated by Django 3.0.5 on 2020-04-10 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet_crawl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='tweet_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
