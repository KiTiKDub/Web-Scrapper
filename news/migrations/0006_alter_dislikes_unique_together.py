# Generated by Django 4.1.7 on 2023-03-13 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_likes_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dislikes',
            unique_together={('article_id', 'user_disliked_id')},
        ),
    ]
