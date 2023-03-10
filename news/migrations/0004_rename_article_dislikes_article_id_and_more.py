# Generated by Django 4.1.7 on 2023-03-08 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_likes_dislikes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dislikes',
            old_name='article',
            new_name='article_id',
        ),
        migrations.RenameField(
            model_name='dislikes',
            old_name='user_disliked',
            new_name='user_disliked_id',
        ),
        migrations.RenameField(
            model_name='likes',
            old_name='article',
            new_name='article_id',
        ),
        migrations.RenameField(
            model_name='likes',
            old_name='user_liked',
            new_name='user_liked_id',
        ),
    ]
