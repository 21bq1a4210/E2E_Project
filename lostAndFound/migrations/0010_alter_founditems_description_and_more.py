# Generated by Django 5.0.1 on 2024-06-26 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostAndFound', '0009_alter_founditems_contact_alter_lostitems_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='founditems',
            name='description',
            field=models.CharField(default=None),
        ),
        migrations.AlterField(
            model_name='lostitems',
            name='description',
            field=models.TextField(default=None),
        ),
    ]
