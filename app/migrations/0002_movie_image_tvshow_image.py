# Generated by Django 4.1.7 on 2023-04-30 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
