from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/search-events/', views.search_events, name='search_events'),
]
