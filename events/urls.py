from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/add/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/update-notes/', views.update_favorite_notes, name='update_favorite_notes'),
]
