from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('parse_and_visualize', views.parse_and_visualize, name="parse_and_visualize"),
    path('generate_and_visualize', views.generate_and_visualize, name="generate_and_visualize"),
    path('search/<str:search_text>/', views.search, name='search'),
    path('filter/<str:filter_text>/', views.filter, name='filter'),
    path('tmdb_search', views.tmdb_search, name='tmdb_search'),
    path('get_graph_data/', views.get_graph_data, name='get_graph_data'),
]
