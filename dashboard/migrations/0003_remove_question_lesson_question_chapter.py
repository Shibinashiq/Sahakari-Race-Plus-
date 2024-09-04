# Generated by Django 4.2.13 on 2024-09-04 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_question_lesson_question_master_question_talenthunt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='lesson',
        ),
        migrations.AddField(
            model_name='question',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.chapter'),
        ),
    ]
