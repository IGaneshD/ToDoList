# Generated by Django 5.0.6 on 2024-06-23 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_taskboard', '0007_alter_task_category_alter_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name="task's Description"),
        ),
    ]
