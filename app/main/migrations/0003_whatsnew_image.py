# Generated by Django 5.0.7 on 2024-07-24 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_whatsnew'),
    ]

    operations = [
        migrations.AddField(
            model_name='whatsnew',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='news'),
        ),
    ]
