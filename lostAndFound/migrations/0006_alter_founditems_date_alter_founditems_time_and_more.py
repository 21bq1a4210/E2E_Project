# Generated by Django 5.0.1 on 2024-06-26 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostAndFound', '0005_alter_founditems_submissionid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='founditems',
            name='date',
            field=models.DateField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='founditems',
            name='time',
            field=models.TimeField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='lostitems',
            name='date',
            field=models.DateField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='lostitems',
            name='time',
            field=models.TimeField(default=None, max_length=200),
        ),
    ]
