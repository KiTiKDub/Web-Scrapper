# Generated by Django 4.1.7 on 2023-03-08 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Likes', to='news.article')),
                ('user_liked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Person', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dislikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Disikes', to='news.article')),
                ('user_disliked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Person_d', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
