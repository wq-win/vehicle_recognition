# Generated by Django 3.1.7 on 2021-03-24 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_super',
            field=models.BooleanField(default=False),
        ),
    ]
