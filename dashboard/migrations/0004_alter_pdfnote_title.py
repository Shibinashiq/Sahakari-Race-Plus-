# Generated by Django 4.2.13 on 2024-08-29 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_rename_title_chapter_chapter_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfnote',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
