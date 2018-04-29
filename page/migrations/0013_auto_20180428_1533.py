# Generated by Django 2.0.4 on 2018-04-28 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0012_merge_20180427_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='photo',
            field=models.ImageField(default='static/images/300x100', upload_to='static/images'),
        ),
        migrations.AlterField(
            model_name='club',
            name='website',
            field=models.CharField(max_length=200),
        ),
    ]
