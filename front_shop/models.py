from django.db import models
# Create your models here.


class RangingCondition(models.Model):
    user_id = models.IntegerField()
    business_id = models.IntegerField()
    api_key = models.CharField(max_length=32, unique=True)
    key_words = models.CharField(max_length=256)
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_date = models.DateField(auto_now_add=True)
    scheduled_start_time = models.TimeField()
    scheduled_end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.api_key


class RankingSearch(models.Model):
    ranking_condition_id = models.ForeignKey(
        RangingCondition, on_delete=models.CASCADE)
    search_date = models.DateField(auto_now_add=True)
    key_words = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.ranking_condition_id


class RankingPalace(models.Model):
    ranking_search_id = models.ForeignKey(
        RankingSearch, on_delete=models.CASCADE)
    rank = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    cid = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(blank=True, null=True)
    rating_total = models.IntegerField(blank=True, null=True)
    price_level = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_name(self, name_list):
        self.name = ','.join(name_list)

    def get_name(self):
        return self.name.split(',')

    def __str__(self):
        return str(self.ranking_search_id)

    def __str__(self) -> str:
        return self.ranking_search_id
