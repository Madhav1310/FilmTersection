import requests
from flask import Flask, render_template, request
from itertools import combinations

app = Flask(__name__)

API_KEY = 'f4484338cde529648772ad772863c20c'  # Your actual TMDB API key
MAX_RECURSION_DEPTH = 50  # Maximum number of API calls per movie (100 recommended movies per movie)

# Global dictionary to store movies and their associated recommendations
global_recommendations = {}

def get_recommendations(movie_name):
    """Fetch the first 20 recommendations for a given movie."""
    print(f"\nCalling TMDB API for movie: {movie_name}")
    
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(search_url).json()

    print(f"Search Response for {movie_name}: {response}")

    if 'results' in response and response['results']:
        movie_id = response['results'][0]['id']
        recommendations_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}"
        recommendations_response = requests.get(recommendations_url).json()

        print(f"Recommendations Response for {movie_name} (ID: {movie_id}): {recommendations_response}")

        if 'results' in recommendations_response:
            return [rec["title"].strip().lower() for rec in recommendations_response["results"][:20]]

    print(f"No recommendations found for {movie_name}")
    return []

def add_to_global_recommendations(movie_name, new_recs):
    """Add new recommendations to the global dictionary for a given movie without duplicates and without adding any movie that is already a key."""
    if movie_name not in global_recommendations:
        global_recommendations[movie_name] = []

    for rec in new_recs:
        if rec not in global_recommendations[movie_name] and rec not in global_recommendations:
            global_recommendations[movie_name].append(rec)

    print(f"\nUpdated Recommendations for {movie_name}: {global_recommendations[movie_name]}")

def find_common_movie():
    """Find a common movie that appears in the recommendation lists of all original movies.
       If no common movie is found across all movies, return the best match across the most movies."""
    movie_keys = list(global_recommendations.keys())
    
    if not movie_keys:
        return None, None
    
    # Check for common movies across all input movies first
    common_movies = set(global_recommendations[movie_keys[0]])

    for key in movie_keys[1:]:
        common_movies.intersection_update(global_recommendations[key])

    if common_movies:
        return common_movies.pop(), movie_keys

    # If no common movie across all, find the best match across the most movies
    max_common_movies = None
    max_combination = None

    for r in range(len(movie_keys) - 1, 0, -1):  # Start from the largest subsets
        for combination in combinations(movie_keys, r):
            common_movies = set(global_recommendations[combination[0]])
            for key in combination[1:]:
                common_movies.intersection_update(global_recommendations[key])

            if common_movies:
                max_common_movies = common_movies
                max_combination = combination
                break
        if max_common_movies:
            break

    if max_common_movies:
        return max_common_movies.pop(), max_combination

    return None, None

def recursive_search(depth=1):
    """Recursively search for a common movie by expanding recommendations. 
    Only look for the best alternative across subsets after reaching MAX_RECURSION_DEPTH."""
    if depth > MAX_RECURSION_DEPTH:
        print("\nMaximum recursion depth reached.")
        # Now check for the best alternative across subsets
        common_movie, common_set = find_common_movie() 
        return common_movie, common_set

    for movie_name, recs in list(global_recommendations.items()):
        if len(recs) >= depth:
            next_movie = recs[depth - 1]
            new_recs = get_recommendations(next_movie)
            add_to_global_recommendations(movie_name, new_recs)

    common_movie, common_set = find_common_movie()
    if common_set and set(common_set) == set(global_recommendations.keys()):
        return common_movie, common_set

    # Continue the search if no common movie across all inputs was found
    return recursive_search(depth + 1)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        global global_recommendations
        global_recommendations = {}

        movies = []
        for i in range(1, 5):
            movie = request.form.get(f"movie{i}")
            if movie:
                movies.append(movie)
                initial_recs = get_recommendations(movie)
                add_to_global_recommendations(movie, initial_recs)

        common_movie, common_set = recursive_search()

        if not common_movie:
            message = "No common movie found across all recommendations."
        else:
            if set(common_set) == set(movies):
                message = f"Common Movie Found: {common_movie}"
            else:
                common_movies_str = ', '.join(common_set)
                message = f"No common movie found across all input movies, but common movie '{common_movie}' found across {common_movies_str}."

        return render_template("movie_map.html", movies=movies, recommendations=global_recommendations, common_movie=common_movie, message=message)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)