# Generated by Django 2.0 on 2018-02-16 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0005_auto_20180216_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='age',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='clarity',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='satisfied',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]