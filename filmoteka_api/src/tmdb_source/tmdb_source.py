import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables from .env file
load_dotenv()


class TmdbDataSource:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        if not self.api_key:
            raise ValueError("TMDB_API_KEY not found in the environment variables.")

        self.base_url = 'https://api.themoviedb.org/3'
        self.headers = {'Content-Type': 'application/json'}

    def _get(self, endpoint, params=None):
        url = f'{self.base_url}/{endpoint}'
        params = params or {}
        params['api_key'] = self.api_key

        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def get_movie_recommendations(self, movie_id):
        endpoint = f'movie/{movie_id}/recommendations'
        params = {'language': 'en-US', 'page': 1}  # You can customize the parameters

        try:
            recommendations = self._get(endpoint, params)['results']
            return recommendations
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie recommendations: {e}")
            return []


if __name__ == "__main__":
    tmdb_data_source = TmdbDataSource()

    movie_id_to_get_recommendations = 466420  # Replace with an actual TMDB movie ID

    recommendations = tmdb_data_source.get_movie_recommendations(movie_id_to_get_recommendations)

    # Store recommendations in a JSON file
    with open('movie_recommendations.json', 'w', encoding='utf-8') as json_file:
        json.dump(recommendations, json_file, ensure_ascii=False, indent=2)
