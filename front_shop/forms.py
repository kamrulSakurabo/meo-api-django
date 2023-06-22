from django import forms
from .models import RangingCondition


class RankingConditionForm(forms.ModelForm):
    class Meta:
        model = RangingCondition
        fields = ['business_id', 'key_words', 'latitude',
                  'longitude',  'scheduled_start_time', 'scheduled_end_time']
