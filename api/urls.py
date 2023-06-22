from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConditionViewSet, GoogleMapView


# router = DefaultRouter()
# router.register(r'range-condition', ConditionViewSet, basename='condition')

urlpatterns = [
    path('range-condition/',
         ConditionViewSet.as_view({'post': 'create'}), name='condition-create'),
    path('range-condition/<str:api_key>/', ConditionViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='condition-detail'),
    path('search/<str:api_key>/', GoogleMapView.as_view(), name='search')

]
