from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('parse_and_visualize', views.parse_and_visualize, name="parse_and_visualize"),
    path('generate_and_visualize', views.generate_and_visualize, name="generate_and_visualize"),
    path('add_filter', views.add_filter, name='add_filter'),
    path('remove_filter/', views.remove_filter, name='remove_filter'),
    path('tmdb_search/', views.tmdb_search, name='tmdb_search'),
    path('get_graph_data/', views.get_graph_data, name='get_graph_data'),
    path('get_graph_attributes/', views.get_graph_attributes, name='get_graph_attributes'),
    path('get_graph_filters/', views.get_graph_filters, name='get_graph_filters'),
]
