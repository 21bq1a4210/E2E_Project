# Generated by Django 5.1.1 on 2024-10-01 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FRS_attendance', '0002_alter_attendance_date_alter_attendance_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Absent', max_length=10),
        ),
    ]
