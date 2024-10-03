# Generated by Django 5.0.6 on 2024-06-19 02:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('complaint_administration', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('user_administration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='escalated_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_administration.escalationstructure'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='groups',
            field=models.ManyToManyField(help_text='The group this complaint belongs to', related_name='complaints', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]