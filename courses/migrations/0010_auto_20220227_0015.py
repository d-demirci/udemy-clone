# Generated by Django 3.1.4 on 2022-02-26 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20220226_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.ManyToManyField(to='courses.Category'),
        ),
    ]
