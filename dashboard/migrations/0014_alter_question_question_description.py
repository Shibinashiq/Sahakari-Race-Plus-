# Generated by Django 4.2.13 on 2024-09-02 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_alter_question_question_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
