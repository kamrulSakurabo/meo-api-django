from django.contrib import admin
from .models import RangingCondition, RankingPalace, RankingSearch
# Register your models here.


class RangingConditionAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'business_id',
                    'api_key',
                    'key_words',
                    'latitude',
                    'longitude',
                    'start_date',
                    'scheduled_start_time',
                    'scheduled_end_time',
                    'created_at',
                    'updated_at',)


admin.site.register(RangingCondition, RangingConditionAdmin)


class RankingSearchAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'ranking_condition_id',
                    'search_date',
                    'latitude',
                    'longitude',
                    'start_datetime',
                    'end_datetime',
                    'status',
                    'created_at',
                    'updated_at',)


admin.site.register(RankingSearch, RankingSearchAdmin)


class RankingPalacehAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'ranking_search_id',
                    'name',
                    'created_at',
                    'updated_at',)

    def get_name(self, obj):
        return obj.name.split(',')

    get_name.short_description = 'Name'


admin.site.register(RankingPalace, RankingPalacehAdmin)
