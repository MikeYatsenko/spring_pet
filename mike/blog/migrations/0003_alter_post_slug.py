# Generated by Django 3.2 on 2021-05-11 17:32

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique_with=['author__name', 'pub_date__month']),
        ),
    ]
