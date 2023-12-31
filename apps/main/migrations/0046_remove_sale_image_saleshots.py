# Generated by Django 4.2 on 2023-10-10 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_alter_news_description_alter_news_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='image',
        ),
        migrations.CreateModel(
            name='SaleShots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='sales', verbose_name='Rasm')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sale')),
            ],
            options={
                'verbose_name': 'Aksiya rasmi',
                'verbose_name_plural': 'Aksiya rasmlari',
            },
        ),
    ]
