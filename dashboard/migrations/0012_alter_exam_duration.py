# Generated by Django 4.2.13 on 2024-09-09 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_alter_exam_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
