from django.contrib import admin
from .models import Condition, Search, Place

# Register your models here.


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_key', 'key_words', 'latitude', 'longitude', 'start_date',
                    'scheduled_start_time', 'scheduled_end_time', 'created_at', 'updated_at']


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ['id',  'condition_id','key_words', 'latitude', 'longitude', 'search_date',
                    'start_datetime', 'end_datetime', 'status', 'created_at', 'updated_at']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['search_id', 'rank', 'name', 'place_id', 'address', 'latitude', 'longitude', 'url',
                    'gmap_url', 'cid', 'rating', 'rating_total', 'price_level', 'category', 'created_at', 'updated_at']
    list_per_page = 20

