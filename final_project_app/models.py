from django.db import models
from django.contrib.postgres.fields import JSONField

  
class THSR(models.Model):
    TrainDate = models.CharField(max_length=100)
    TrainNo = models.CharField(max_length=100)
    Direction = models.IntegerField()
    StartingStationID = models.CharField(max_length=100)
    StartingStationName = models.CharField(max_length=100)
    EndingStationID = models.CharField(max_length=100)
    EndingStationName = models.CharField(max_length=100)
    StopSequence = models.IntegerField()
    ArrivalTime = models.CharField(max_length=100)
    DepartureTime = models.CharField(max_length=100)
    
class THSR_Schedule(models.Model):
    UpdateTime = models.CharField(max_length=100)
    EffectiveDate = models.CharField(max_length=100)
    ExpiringDate = models.CharField(max_length=100)
    VersionID = models.IntegerField()
    
    # GeneralTrainInfo
    TrainNo = models.CharField(max_length=10)
    Direction = models.IntegerField()
    StartingStationID = models.CharField(max_length=10)
    StartingStationName_zh_tw = models.CharField(max_length=50)
    StartingStationName_en = models.CharField(max_length=50)
    EndingStationID = models.CharField(max_length=10)
    EndingStationName_zh_tw = models.CharField(max_length=50)
    EndingStationName_en = models.CharField(max_length=50)
    
    # ServiceDay
    Monday = models.BooleanField()
    Tuesday = models.BooleanField()
    Wednesday = models.BooleanField()
    Thursday = models.BooleanField()
    Friday = models.BooleanField()
    Saturday = models.BooleanField()
    Sunday = models.BooleanField()
    
    SrcUpdateTime = models.DateTimeField()

class StopTime(models.Model):
    schedule = models.ForeignKey(THSR_Schedule, related_name='stop_times', on_delete=models.CASCADE)
    StopSequence = models.IntegerField()
    StationID = models.CharField(max_length=10)
    StationName_zh_tw = models.CharField(max_length=50)
    StationName_en = models.CharField(max_length=50)
    ArrivalTime = models.TimeField(null=True, blank=True)
    DepartureTime = models.TimeField(null=True, blank=True)

    

    
class TRA(models.Model):
    TrainNo = models.CharField(max_length=100)
    Direction = models.IntegerField()
    StartingStationID = models.CharField(max_length=100)
    StartingStationName = models.CharField(max_length=100)
    EndingStationID = models.CharField(max_length=100)
    EndingStationName = models.CharField(max_length=100)
    TrainTypeName = models.CharField(max_length=100)
    TripLine = models.IntegerField()
    PackageServiceFlag = models.BooleanField()
    DailyFlag = models.BooleanField()
    

class Metro(models.Model):
    RouteID = models.CharField(max_length=100)
    StationID = models.CharField(max_length=100)
    StationName = models.CharField(max_length=100)
    Direction = models.IntegerField()
    DestinationStaionID = models.CharField(max_length=100)
    DestinationStationName = models.CharField(max_length=100)
    Sequence = models.IntegerField()
    ArrivalTime = models.CharField(max_length=100)
    DepartureTime = models.CharField(max_length=100)
    TrainType = models.IntegerField()
    
class THSRODFare(models.Model):
    OriginStationID = models.CharField(max_length=100)
    OriginStationName = models.CharField(max_length=100)
    DestinationStationID = models.CharField(max_length=100)
    DestinationStationName = models.CharField(max_length=100)
    TicketType = models.IntegerField()
    FareClass = models.IntegerField()
    CabinClass = models.IntegerField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    
class TRAODFare(models.Model):
    OriginStationID = models.CharField(max_length=100)
    OriginStationName = models.CharField(max_length=100)
    DestinationStationID = models.CharField(max_length=100)
    DestinationStationName = models.CharField(max_length=100)
    TicketType = models.CharField(max_length=100)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    
class Image(models.Model):
    Geometry = models.CharField(max_length = 100 , null = "N/A")
    
    
class Metro_sta(models.Model):
    StationID = models.CharField(max_length = 100 , null = "N/A")
    StationName_Zh_tw = models.CharField(max_length = 100 , null = "N/A")
    
class Metro_sta_to_sta(models.Model):
    FromStationID = models.CharField(max_length = 100 , null = "N/A")
    FromStationName_Zh_tw = models.CharField(max_length = 100 , null = "N/A")
    ToStationID = models.CharField(max_length = 100 , null = "N/A")
    ToStationName_Zh_tw = models.CharField(max_length = 100 , null = "N/A")
    RunTime = models.IntegerField()
    StopTime = models.IntegerField()
