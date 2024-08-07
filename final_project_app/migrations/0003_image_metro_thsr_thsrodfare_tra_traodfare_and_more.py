# Generated by Django 4.2.1 on 2023-06-07 17:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("final_project_app", "0002_train_ticket"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
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
                ("Geometry", models.CharField(max_length=100, null="N/A")),
            ],
        ),
        migrations.CreateModel(
            name="Metro",
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
                ("RouteID", models.CharField(max_length=100)),
                ("StationID", models.CharField(max_length=100)),
                ("StationName", models.CharField(max_length=100)),
                ("Direction", models.IntegerField()),
                ("DestinationStationID", models.CharField(max_length=100)),
                ("DestinationStationName", models.CharField(max_length=100)),
                ("Sequence", models.IntegerField()),
                ("ArrivalTime", models.CharField(max_length=100)),
                ("DepartureTime", models.CharField(max_length=100)),
                ("TrainType", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="THSR",
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
                ("TrainDate", models.CharField(max_length=100)),
                ("TrainNo", models.CharField(max_length=100)),
                ("Direction", models.IntegerField()),
                ("StartingStationID", models.CharField(max_length=100)),
                ("StartingStationName", models.CharField(max_length=100)),
                ("EndingStationID", models.CharField(max_length=100)),
                ("EndingStationName", models.CharField(max_length=100)),
                ("StopSequence", models.IntegerField()),
                ("ArrivalTime", models.CharField(max_length=100)),
                ("DepartureTime", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="THSRODFare",
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
                ("OriginStationID", models.CharField(max_length=100)),
                ("OriginStationName", models.CharField(max_length=100)),
                ("DestinationStationID", models.CharField(max_length=100)),
                ("DestinationStationName", models.CharField(max_length=100)),
                ("TicketType", models.IntegerField()),
                ("FareClass", models.IntegerField()),
                ("CabinClass", models.IntegerField()),
                ("Price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="TRA",
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
                ("TrainNo", models.CharField(max_length=100)),
                ("Direction", models.IntegerField()),
                ("StartingStationID", models.CharField(max_length=100)),
                ("StartingStationName", models.CharField(max_length=100)),
                ("EndingStationID", models.CharField(max_length=100)),
                ("EndingStationName", models.CharField(max_length=100)),
                ("TrainTypeName", models.CharField(max_length=100)),
                ("TripLine", models.IntegerField()),
                ("PackageServiceFlag", models.BooleanField()),
                ("DailyFlag", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="TRAODFare",
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
                ("OriginStationID", models.CharField(max_length=100)),
                ("OriginStationName", models.CharField(max_length=100)),
                ("DestinationStationID", models.CharField(max_length=100)),
                ("DestinationStationName", models.CharField(max_length=100)),
                ("TicketType", models.CharField(max_length=100)),
                ("Price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.DeleteModel(
            name="train_Station",
        ),
        migrations.DeleteModel(
            name="train_ticket",
        ),
    ]
