# Generated by Django 4.1.7 on 2023-03-05 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=256)),
                ('body', models.CharField(max_length=5000)),
                ('category', models.CharField(max_length=32)),
                ('url', models.URLField()),
                ('search', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Query', to='news.query')),
            ],
        ),
    ]
