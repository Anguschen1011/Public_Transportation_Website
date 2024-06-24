# Generated by Django 4.2.1 on 2023-06-08 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("final_project_app", "0005_thsr_schedule"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="thsr_schedule",
            name="ArrivalTime",
        ),
        migrations.RemoveField(
            model_name="thsr_schedule",
            name="DepartureTime",
        ),
        migrations.RemoveField(
            model_name="thsr_schedule",
            name="StationID",
        ),
        migrations.RemoveField(
            model_name="thsr_schedule",
            name="StationName_en",
        ),
        migrations.RemoveField(
            model_name="thsr_schedule",
            name="StationName_zh_tw",
        ),
        migrations.RemoveField(
            model_name="thsr_schedule",
            name="StopSequence",
        ),
        migrations.CreateModel(
            name="StopTime",
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
                ("StopSequence", models.IntegerField()),
                ("StationID", models.CharField(max_length=10)),
                ("StationName_zh_tw", models.CharField(max_length=50)),
                ("StationName_en", models.CharField(max_length=50)),
                ("ArrivalTime", models.TimeField(blank=True, null=True)),
                ("DepartureTime", models.TimeField(blank=True, null=True)),
                (
                    "schedule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stop_times",
                        to="final_project_app.thsr_schedule",
                    ),
                ),
            ],
        ),
    ]
