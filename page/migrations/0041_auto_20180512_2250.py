# Generated by Django 2.0.4 on 2018-05-13 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0040_auto_20180512_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='email',
            field=models.EmailField(max_length=30),
        ),
        migrations.AlterField(
            model_name='club',
            name='website',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='interview',
            name='text',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='leader',
            name='email',
            field=models.EmailField(max_length=40),
        ),
        migrations.AlterField(
            model_name='leader',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='leader',
            name='title',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(max_length=2000),
        ),
    ]
