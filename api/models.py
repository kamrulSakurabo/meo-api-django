from django.db import models
from django.utils import timezone


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Condition(BaseModel):
    api_key = models.CharField(max_length=32, unique=True)
    key_words = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_date = models.DateField(auto_now_add=True)
    scheduled_start_time = models.TimeField()
    scheduled_end_time = models.TimeField()

    def __str__(self):
        return f'{self.api_key}{self.key_words}@{self.latitude}/{self.longitude}'


class Search(BaseModel):
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    search_date = models.DateField(auto_now_add=True)
    key_words = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, default='wait')

    def __str__(self):
        return f'<Search {self.id} {self.condition_id}:{self.search_date}>'


class Place(BaseModel):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    rank = models.IntegerField()
    name = models.CharField(max_length=255, blank=True)
    place_id = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    url = models.URLField(max_length=255, blank=True, null=True)
    gmap_url = models.URLField(max_length=1024 ,blank=True, null=True)
    cid = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(blank=True, null=True)
    rating_total = models.IntegerField(blank=True, null=True)
    price_level = models.IntegerField( null=True, blank=True)
    category = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'<Place {self.id}{self.name}{self.search_id}>'
