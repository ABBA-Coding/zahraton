# Generated by Django 4.1.4 on 2023-04-12 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_order_do_num_order_doc_entry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='do_num',
            new_name='doc_num',
        ),
    ]
