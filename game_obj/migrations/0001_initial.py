# Generated by Django 4.0.3 on 2022-03-21 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('hand_name', models.CharField(max_length=100)),
                ('hand', models.CharField(max_length=200)),
                ('stack', models.IntegerField()),
                ('phase', models.CharField(max_length=200)),
            ],
        ),
    ]
