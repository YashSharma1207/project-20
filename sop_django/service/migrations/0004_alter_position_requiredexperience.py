# Generated by Django 4.2.19 on 2025-02-13 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='requiredExperience',
            field=models.IntegerField(),
        ),
    ]
