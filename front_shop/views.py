from typing import Any, Optional
from django.db import models
from django.http import JsonResponse
import requests
import datetime
import json
from hashlib import sha256
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic import ListView, UpdateView, DeleteView, FormView
from .models import RangingCondition, RankingSearch, RankingPalace
from .forms import RankingConditionForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.utils.timezone import make_aware
import traceback


from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed


class CreateConditionView(FormView):
    template_name = 'condition_form.html'

    def get(self, request):
        form = RankingConditionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RankingConditionForm(request.POST)
        if form.is_valid():
            condition = form.save(commit=False)
            condition.user_id = request.user.id

            # API request url
            url = f"http://localhost:8000/api/range-condition/"
            headers = {'Content-Type': 'application/json'}

            # Data to be sent to API

            data = {
                'user_id': condition.user_id,
                'business_id': condition.business_id,
                'key_words': condition.key_words,
                'latitude': condition.latitude,
                'longitude': condition.longitude,
                'scheduled_start_time': condition.scheduled_start_time.strftime('%H:%M:%S'),
                'scheduled_end_time': condition.scheduled_end_time.strftime('%H:%M:%S'),
            }

            # Send the request to the API

            response = requests.post(url, json=data, headers=headers)
            print(response)

            if response.status_code == 201:
                api_key = response.json().get('api_key')
                condition.api_key = api_key
                condition.save()
                messages.success(request, 'Data saved successfully!')
                return redirect('list')

            else:
                messages.error(
                    request, 'Data could not be sent. An error occurred!')
                print(data)
                return redirect('/')

        return render(request, self.template_name, {'form': form})


class List_view(ListView):
    model = RangingCondition
    queryset = RangingCondition.objects.all().only('id', 'key_words', 'latitude',
                                                   'longitude', 'scheduled_start_time', 'scheduled_end_time')
    template_name = 'front_shop/success.html'


class ConditionUpdateView(UpdateView):
    model = RangingCondition
    fields = ['key_words', 'latitude', 'longitude',
              'scheduled_start_time', 'scheduled_end_time']
    template_name = 'front_shop/update.html'
    success_url = reverse_lazy('list')

    def get_object(self, queryset=None):
        api_key = self.kwargs.get('api_key')
        return get_object_or_404(RangingCondition, api_key=api_key)

    def form_valid(self, form):
        response = requests.put(
            f'http://localhost:8000/api/range-condition/{self.object.api_key}/', data=form.cleaned_data)
        # print(response.text)
        print(form.cleaned_data)
        if response.status_code == 200:
            data = response.json()
            print(data)
            self.object.api_key = data.get('api_key', self.object.api_key)
            self.object.save()
            return super().form_valid(form)
        else:
            form.add_error(None, 'There was an error with the API request.')
            return super().form_invalid(form)


def condition_delete_view(request, api_key):
    if request.method == 'POST':
        condition = get_object_or_404(RangingCondition, api_key=api_key)

        response = requests.delete(
            f'http://localhost:8000/api/range-condition/{condition.api_key}/')

        if response.status_code == 204:
            condition.delete()
            return redirect(reverse('list'))
        else:
            messages.error(
                request, f'Ther was an error with API request Condition could not be deleted')
            return redirect(reverse('list'))
    else:
        return HttpResponseNotAllowed(['POST'])


@method_decorator(csrf_exempt, name='dispatch')
class SearchView(View):
    def get(self, request, api_key):
        try:
            condition = RangingCondition.objects.get(api_key=api_key)

            if not condition.latitude or not condition.longitude or not condition.key_words:
                return JsonResponse({"error": "Invalid latitude, longitude, or keywords"}, status=400)

            response = requests.get(
                f'http://localhost:8000/api/search/{condition.api_key}/')
            print("Response:", response.json())

            if response.status_code == 200:
                search_data = response.json()
                print('search data:', search_data)

                for search_datum in search_data:
                    start_datetime_str = search_data['start_datetime']
                    start_datetime = datetime.datetime.strptime(
                        start_datetime_str, "%Y-%m-%dT%H:%M:%S%z")
                    start_datetime = make_aware(start_datetime)

                    end_datetime_str = search_data['end_datetime']
                    end_datetime = datetime.datetime.strptime(
                        end_datetime_str, "%Y-%m-%dT%H:%M:%S%z")
                    start_datetime = make_aware(start_datetime)

                    ranking_search = RankingSearch.objects.create(
                        ranking_condition_id=condition,
                        # search_date=['search_date'],
                        key_words=search_data['key_words'],
                        latitude=search_data['latitude'],
                        longitude=search_data['longitude'],
                        start_datetime=start_datetime,
                        end_datetime=end_datetime,
                        # start_datetime=datetime.datetime.strptime(search_data['start_datetime'], "%H:%M:%S").time(),
                        # end_datetime=datetime.datetime.strptime(search_data['end_datetime'], "%H:%M:%S").time(),
                        status='completed' if search_data['search_result'] == 'Search complete' else 'failed',
                    )
                    ranking_search.save()
                    print('Search Data saved successfully')

                    for place_data in search_datum['places']:
                        try:
                            palace = RankingPalace.objects.create(
                                ranking_search_id=ranking_search,
                                rank=place_data['rank'],
                                name=place_data['name'],
                                latitude=place_data['latitude'],
                                longitude=place_data['longitude'],
                                cid=place_data['cid'],
                                rating=place_data['rating'],
                                rating_level=place_data['rating_level'],
                                category=place_data['category'],
                            )
                            print("Created RankingPalace:", palace)

                        except Exception as e:
                            print('Data:', search_data)
                            print("Error", str(e))
                            return JsonResponse({"error": f"Error in creating RankingSearch object: {str(e)}"}, status=500)

                return render(request, "front_shop/search_result.html",  {"data": search_data})
            else:
                return JsonResponse({"error": "There was an error with the API request"}, status=500)
        except RangingCondition.DoesNotExist:
            return JsonResponse({"error": "Condition with provided API Key does not exist"}, status=400)

    def post(self, request, api_key):
        try:
            data = json.loads(request.body)
            print('Data received in POST request:', data)
            condition = RangingCondition.objects.get(api_key=api_key)

            start_datetime_str = data['start_datetime']
            start_datetime = datetime.datetime.strptime(
                start_datetime_str, "%Y-%m-%dT%H:%M:%S%z")

            end_datetime_str = data['end_datetime']
            end_datetime = datetime.datetime.strptime(
                end_datetime_str, "%Y-%m-%dT%H:%M:%S%z")

            ranking_search = RankingSearch.objects.create(
                ranking_condition_id=condition,
                key_words=data['key_words'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                status='completed' if data['search_result'] == 'Search complete' else 'failed',
            )
            print('Data saved successfully')
            if 'places' not in data or type(data['places']) is not list:
                return JsonResponse({"error": "Incorrect or missing 'places' data"}, status=400)
            print('Data received in Post request', data)

            if 'places' in data:
                for place_data in data['places']:
                    print("Creating RankingPalace with data:", place_data)
                    try:
                        palace = RankingPalace.objects.create(
                            ranking_search_id=ranking_search,
                            rank=place_data['rank'],
                            name=place_data['name'],
                            latitude=place_data['latitude'],
                            longitude=place_data['longitude'],
                            cid=place_data['cid'],
                            rating=place_data['rating'],
                            # price_level=place_data['rating_level'],
                            category=place_data['category'],
                        )
                        print("Created RankingPalace:", palace)
                    except Exception as e:
                        print("Failed to create RankingPalace:", str(e))
            return JsonResponse({"message": "Data saved successfully"}, status=200)

        except RangingCondition.DoesNotExist:
            return JsonResponse({"error": "Condition with provided API Key does not exist"}, status=400)
        except Exception as e:
            print('Full Traceback:\n', traceback.format_exc())
            return JsonResponse({"error": f"Error in processing POST request: {str(e)}"}, status=500)
