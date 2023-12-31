# Generated by Django 4.2 on 2023-08-03 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_alter_news_for_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10000, null=True)),
                ('description', models.CharField(blank=True, max_length=10000, null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('all_chats', models.IntegerField(default=0)),
            ],
        ),
    ]
