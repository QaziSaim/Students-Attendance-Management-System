# Generated by Django 4.1.4 on 2023-02-04 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AMS', '0010_attendance_student_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='staff_username',
            field=models.CharField(default=True, max_length=100),
            preserve_default=False,
        ),
    ]
