from rest_framework import serializers
from django.utils import timezone
from . models import Condition, Search, Place, BaseModel


class BaseModelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = BaseModel
        fields = '__all__'

class ConditionSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(read_only=True)
    api_key = serializers.CharField(read_only=True)

    class Meta:
        model = Condition
        fields = '__all__'
        #  exclude = ['start_date']


class SearchSerializer(serializers.ModelSerializer):
    # start_datetime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    # end_datetime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    class Meta:
        model = Search
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
