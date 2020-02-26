# Generated by Django 3.0.3 on 2020-02-25 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fullgame', '0005_auto_20200225_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='gamecategory',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
    ]