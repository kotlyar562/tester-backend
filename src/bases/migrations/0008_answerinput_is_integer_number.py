# Generated by Django 2.0.5 on 2018-06-20 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bases', '0007_auto_20180620_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerinput',
            name='is_integer_number',
            field=models.BooleanField(default=False, verbose_name='Целое число?'),
        ),
    ]