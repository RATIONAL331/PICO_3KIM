# Generated by Django 3.0.5 on 2020-04-27 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0003_auto_20200427_2048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ('upload_dt',)},
        ),
    ]
