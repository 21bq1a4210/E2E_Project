# Generated by Django 5.0.1 on 2024-06-26 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostAndFound', '0006_alter_founditems_date_alter_founditems_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lostitems',
            name='image',
            field=models.ImageField(blank=True, default=None, max_length=200, upload_to='lostitems/'),
        ),
    ]
