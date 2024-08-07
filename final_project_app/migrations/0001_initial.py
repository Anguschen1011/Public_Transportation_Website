# Generated by Django 4.2.1 on 2023-06-01 07:00

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="train_Station",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("TrainNo", models.BigIntegerField(default=-1)),
                ("StationID", models.BigIntegerField(default=-1)),
                ("StationName", models.CharField(default="N/A", max_length=100)),
                ("DelayTime", models.BigIntegerField(default=-1)),
                ("SrcUpdateTime", models.DateTimeField(default=None)),
                ("UpdateTime", models.DateTimeField(default=None)),
            ],
        ),
    ]
