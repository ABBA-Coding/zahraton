# Generated by Django 4.2 on 2023-10-10 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_alter_news_options_alter_notification_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
