# Generated by Django 4.1.4 on 2023-02-04 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AMS', '0009_remove_attendance_session_year_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='student_id',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to='AMS.student'),
            preserve_default=False,
        ),
    ]
