from django.http import JsonResponse
from django.shortcuts import render
from django.apps import apps
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
import json
import os
import requests


def index(request):
    return render(request, 'index.html', None)


@csrf_exempt
def generate_and_visualize(request):
    try:
        request_data = json.loads(request.body)
        search_value = request_data.get('search', None)
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request data'}, status=400)

    generate_data_plugin = "tmdb_source"
    parse_data_plugin = "json_parser"
    data_source_plugins = apps.get_app_config('filmoteka_platform').data_source_plugins
    visualize_plugin = apps.get_app_config('filmoteka_platform').visualizer_plugins

    generate_plugin = next((plugin for plugin in data_source_plugins if plugin.identifier() == generate_data_plugin),
                           None)
    if generate_plugin:
        generate_plugin.fetch_data(search_value, "7cafc24ef4102576b372a59dd9edfbf2")
    else:
        return JsonResponse({'error': f'Plugin {generate_data_plugin} not found'}, status=404)

    parse_plugin = next((plugin for plugin in data_source_plugins if plugin.identifier() == parse_data_plugin), None)
    if parse_plugin:
        template_dir = os.path.join(os.path.dirname(__file__), '..', '..')
        json_path = os.path.join(template_dir, 'movie_recommendations.json')
        graph = parse_plugin.parse(json_path)
    else:
        return JsonResponse({'error': f'Plugin {parse_data_plugin} not found'}, status=404)

    visualize_plugin = next((plugin for plugin in visualize_plugin if plugin.identifier() == "Block_Visualizer"), None)
    if visualize_plugin:
        html_output = visualize_plugin.visualize(graph)
        return HttpResponse(html_output)
    else:
        return JsonResponse({'error': f'Plugin Block_Visualizer not found'}, status=404)


@csrf_exempt
@require_GET
def tmdb_search(request):
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'results': []})

    tmdb_key = '7cafc24ef4102576b372a59dd9edfbf2'
    endpoint = 'search/movie'
    params = {'query': query, 'language': 'en-US', 'page': 1, 'api_key': tmdb_key}

    try:
        response = requests.get(f'https://api.themoviedb.org/3/{endpoint}', params=params,
                                headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        search_results = response.json()
        return JsonResponse({'results': search_results['results']})
    except requests.exceptions.RequestException as e:
        print(f"Error searching for movie: {e}")
        return JsonResponse({'results': []})


def parse_and_visualize():
    return None


def search():
    return None


def filter():
    return None
