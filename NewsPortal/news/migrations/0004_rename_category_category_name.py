# Generated by Django 5.0.4 on 2024-06-01 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_rename_name_category_category_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='name',
        ),
    ]
