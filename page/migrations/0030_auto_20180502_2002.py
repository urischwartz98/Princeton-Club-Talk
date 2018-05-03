# Generated by Django 2.0.4 on 2018-05-03 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0029_auto_20180502_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='club_interviews_reviewed',
            field=models.ManyToManyField(blank=True, null=True, related_name='interviews', to='page.Club'),
        ),
        migrations.AlterField(
            model_name='student',
            name='clubs_interested',
            field=models.ManyToManyField(blank=True, null=True, related_name='interested', to='page.Club'),
        ),
        migrations.AlterField(
            model_name='student',
            name='clubs_liked',
            field=models.ManyToManyField(blank=True, null=True, related_name='likes', to='page.Club'),
        ),
        migrations.AlterField(
            model_name='student',
            name='clubs_reviewed',
            field=models.ManyToManyField(blank=True, null=True, related_name='submissions', to='page.Club'),
        ),
        migrations.AlterField(
            model_name='student',
            name='review_votes',
            field=models.ManyToManyField(blank=True, null=True, related_name='votes', to='page.Review'),
        ),
    ]