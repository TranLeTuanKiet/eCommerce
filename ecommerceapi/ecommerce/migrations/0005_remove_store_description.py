# Generated by Django 5.0.4 on 2024-05-15 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_remove_buyer_groups_remove_buyer_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='description',
        ),
    ]
