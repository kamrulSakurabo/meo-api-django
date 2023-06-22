from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateConditionView.as_view(), name='condition'),
    path('list/', views.List_view.as_view(), name='list'),
    path('delete/<str:api_key>/', views.condition_delete_view, name='delete'),
    path('update/<str:api_key>/', views.ConditionUpdateView.as_view(),
         name='condition-update'),
    path('search/<str:api_key>/', views.SearchView.as_view(), name='search'),
]
