# Generated by Django 4.2.13 on 2024-08-30 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_pdfnote_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
