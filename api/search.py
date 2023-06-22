from drivers.driver import get_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .serializers import PlaceSerializer, SearchSerializer
from .models import Condition, Search, Place
from .scraper import Scraper
from django.utils import timezone
from time import sleep


def search_in_google_map(condition):
    latitude = condition.latitude
    longitude = condition.longitude
    key_words = condition.key_words
    num_places = 20

    print(
        f"Debug: Condition: {condition}, Latitude: {latitude}, Longitude: {longitude}, Key words: {key_words}")

    if latitude is None or longitude is None:
        return 'Invalid latitude or longitude'

    scraper = Scraper(key_words, latitude, longitude,num_places)

    # Create and save the Search model instance
    search_serializer = SearchSerializer(data={
        'condition': condition.id,
        'key_words': key_words,
        'latitude': latitude,
        'longitude': longitude,
        'status': 'running',
        'start_datetime': timezone.now()
    })

    if search_serializer.is_valid():
        search_serializer.save()
    else:
        print('Invalid data:', search_serializer.errors)
        return 'Search creation failed'

    places = scraper.scrape_places()

    if places:
        for rank, place in enumerate(places, start=1):
            place_data = place
            place_data.update({
                'search': search_serializer.instance.id,
                'rank': rank,
                'latitude': condition.latitude,
                'longitude': condition.longitude,
            })

            place_serializer = PlaceSerializer(data=place_data)

            if place_serializer.is_valid():
                place_serializer.save()

            else:
                print('Invalid data', place_serializer.errors)

        search_serializer.instance.status = 'Done'
        search_serializer.instance.end_datetime = timezone.now()
        search_serializer.instance.save()
    else:
        print("No places found")
        search_serializer.instance.status = 'failed'
        search_serializer.instance.end_datetime = timezone.now()
        search_serializer.instance.save()
    return 'Search complete'
