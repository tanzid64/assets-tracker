# Generated by Django 5.0.3 on 2024-03-27 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicelog',
            name='checked_out_condition',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]