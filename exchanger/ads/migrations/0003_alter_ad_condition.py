# Generated by Django 5.2.4 on 2025-07-14 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_ad_category_alter_ad_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='condition',
            field=models.CharField(choices=[('new', 'Новый'), ('used', 'Б/у')], max_length=20),
        ),
    ]
