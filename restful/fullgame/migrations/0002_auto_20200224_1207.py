# Generated by Django 3.0.3 on 2020-02-24 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fullgame', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamecategory',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]