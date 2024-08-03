import requests
import json

from api.tmdb_source_api import DataSourceAPI


class TmdbDataSource(DataSourceAPI):

    def name(self):
        return "TMDB Source"

    def identifier(self):
        return "tmdb_source"

    def fetch_data(self, movie_name: str, tmdb_key: str):
        # Get the movie ID from the name
        movie_id = self.get_movie_id_by_name(movie_name, tmdb_key)
        if not movie_id:
            print(f"Movie with name '{movie_name}' not found.")
            return

        # Fetch the main movie details
        main_movie = self.get_movie_details(movie_id, tmdb_key)

        # Fetch the recommendations with depth
        recommendations = self.get_movie_recommendations_depth(movie_id, tmdb_key, 2)

        # Add the recommendations as children of the main movie
        main_movie['child'] = recommendations

        # Save the entire structure to a JSON file
        with open('../movie_recommendations.json', 'w', encoding='utf-8') as json_file:
            json.dump(main_movie, json_file, ensure_ascii=False, indent=2)

    def _get(self, endpoint, tmdb_key, params=None):
        url = "https://api.themoviedb.org/3/" + endpoint
        params = params or {}
        params['api_key'] = tmdb_key

        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})
        response.raise_for_status()

        return response.json()

    def get_movie_id_by_name(self, movie_name, tmdb_key):
        """Searches for a movie by name and returns the ID of the first result."""
        endpoint = 'search/movie'
        params = {'query': movie_name, 'language': 'en-US', 'page': 1}

        try:
            search_results = self._get(endpoint, tmdb_key, params)['results']
            if search_results:
                return search_results[0]['id']  # Return the ID of the first movie in the list
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error searching for movie by name: {e}")
            return None

    def get_movie_details(self, movie_id, tmdb_key):
        """Fetches the details of the main movie."""
        endpoint = f'movie/{movie_id}'
        try:
            movie_details = self._get(endpoint, tmdb_key)
            # We want only specific details
            main_movie = {
                "ID": movie_details['id'],
                "Original Title": movie_details['original_title'],
                "Popularity": movie_details['popularity'],
                "Release Date": movie_details['release_date']
            }
            return main_movie
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie details: {e}")
            return {}

    def get_movie_recommendations_depth(self, movie_id, tmdb_key, depth):
        if depth == 0:
            return []

        recommendations = self.get_movie_recommendations(movie_id, tmdb_key)
        all_recommendations = []

        for recommendation in recommendations:
            recommendation_id = recommendation['id']
            child_recommendations = self.get_movie_recommendations_depth(recommendation_id, tmdb_key, depth - 1)

            recommendation_dict = {
                "ID": recommendation_id,
                "Original Title": recommendation['original_title'],
                "Popularity": recommendation['popularity'],
                "Release Date": recommendation['release_date']
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
