# Generated by Django 4.2 on 2023-08-03 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='name',
        ),
    ]