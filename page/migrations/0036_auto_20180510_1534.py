# Generated by Django 2.0.4 on 2018-05-10 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0035_auto_20180508_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='desc',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='interview',
            name='text',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(max_length=5000),
        ),
    ]