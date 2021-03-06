# Generated by Django 3.0.5 on 2020-04-10 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('tweet_id', models.IntegerField(max_length=200, primary_key=True, serialize=False)),
                ('picture_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateField()),
                ('pictures', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweet_crawl.Picture')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
