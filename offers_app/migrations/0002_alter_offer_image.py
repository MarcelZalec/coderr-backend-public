# Generated by Django 5.1.7 on 2025-04-11 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='uploads/orders/'),
        ),
    ]
