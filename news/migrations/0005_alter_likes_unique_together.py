# Generated by Django 4.1.7 on 2023-03-12 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_rename_article_dislikes_article_id_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='likes',
            unique_together={('article_id', 'user_liked_id')},
        ),
    ]
