import requests
import json

from api.tmdb_source_api import DataSourceAPI


class TmdbDataSource(DataSourceAPI):

    def name(self):
        return "TMDB Source"

    def identifier(self):
        return "tmdb_source"

    def fetch_data(self, movie_id: str, tmdb_key: str):
        recommendations = self.get_movie_recommendations_depth(movie_id, tmdb_key, 2)
        with open('../movie_recommendations.json', 'w', encoding='utf-8') as json_file:
            json.dump(recommendations, json_file, ensure_ascii=False, indent=2)

    def _get(self, endpoint, tmdb_key, params=None):
        url = "https://api.themoviedb.org/3/" + endpoint
        params = params or {}
        params['api_key'] = tmdb_key

        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})
        response.raise_for_status()

        return response.json()

    def get_movie_recommendations_depth(self, movie_id, tmdb_key, depth):
        if depth == 0:
            return []

        recommendations = self.get_movie_recommendations(movie_id, tmdb_key)
        all_recommendations = []

        for recommendation in recommendations:
            recommendation_id = recommendation['id']
            child_recommendations = self.get_movie_recommendations_depth(recommendation_id, tmdb_key, depth - 1)

            recommendation_dict = {
                "id": recommendation_id,
                "original_title": recommendation['original_title'],
                "overview": recommendation['overview'],
                "vote_average": recommendation['vote_average'],
                "release_date": recommendation['release_date']
            }

            if child_recommendations:
                recommendation_dict["child"] = child_recommendations

            all_recommendations.append(recommendation_dict)

        return all_recommendations

    def get_movie_recommendations(self, movie_id, tmdb_key):
        endpoint = f'movie/{movie_id}/recommendations'
        params = {'language': 'en-US', 'page': 1}  # You can customize the parameters

        try:
            recommendations = self._get(endpoint, tmdb_key, params)['results']
            return recommendations
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie recommendations: {e}")
            return []

# if __name__ == "__main__":
#     tmdb_data_source = TmdbDataSource()
#
#     movie_id_to_get_recommendations = 466420  # Replace with an actual TMDB movie ID
#
#     recommendations = tmdb_data_source.get_movie_recommendations_depth(movie_id_to_get_recommendations, 2)
#
#     # Store recommendations in a JSON file
#     with open('../movie_recommendations.json', 'w', encoding='utf-8') as json_file:
#         json.dump(recommendations, json_file, ensure_ascii=False, indent=2)
