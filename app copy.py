import requests
from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)

API_KEY = 'f4484338cde529648772ad772863c20c'  # Your actual TMDB API key
MAX_RECURSION_DEPTH = 5  # Maximum number of API calls per movie (100 recommended movies per movie)

# Global dictionary to store movies and their associated recommendations
global_recommendations = {}

def get_recommendations(movie_name):
    """Fetch the first 20 recommendations for a given movie."""
    # Debug statement to indicate an API call is being made
    print(f"\nCalling TMDB API for movie: {movie_name}")
    
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(search_url).json()

    # Debug statement to show the search response
    print(f"Search Response for {movie_name}: {response}")

    if 'results' in response and response['results']:
        movie_id = response['results'][0]['id']
        recommendations_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}"
        recommendations_response = requests.get(recommendations_url).json()

        # Debug statement to show the recommendations response
        print(f"Recommendations Response for {movie_name} (ID: {movie_id}): {recommendations_response}")

        if 'results' in recommendations_response:
            return [rec["title"].strip().lower() for rec in recommendations_response["results"][:20]]

    # Debug statement if no recommendations are found
    print(f"No recommendations found for {movie_name}")
    return []

def add_to_global_recommendations(movie_name, new_recs):
    """Add new recommendations to the global dictionary for a given movie without duplicates and without adding any movie that is already a key."""
    if movie_name not in global_recommendations:
        global_recommendations[movie_name] = []

    # Add only unique recommendations that are not already keys in the global dictionary
    for rec in new_recs:
        if rec not in global_recommendations[movie_name] and rec not in global_recommendations:
            global_recommendations[movie_name].append(rec)

    # Debug statement to show the updated global recommendations
    print(f"\nUpdated Recommendations for {movie_name}: {global_recommendations[movie_name]}")

def find_common_movie():
    """Find a common movie that appears in the recommendation lists of all original movies."""
    # Create a set of movies that appear in the recommendation list of the first movie
    common_movies = set(global_recommendations[next(iter(global_recommendations))])

    # Intersect this set with the recommendation lists of all other movies
    for recs in global_recommendations.values():
        common_movies.intersection_update(recs)

    # If there's any movie left in the intersection, it's common to all movies
    if common_movies:
        common_movie = common_movies.pop()
        # Debug statement to show the found common movie
        print(f"\nCommon Movie Found: {common_movie}")
        return common_movie

    # Debug statement if no common movie is found
    print("\nNo common movie found.")
    return None

def recursive_search(depth=1):
    """Recursively search for a common movie by expanding recommendations."""
    if depth > MAX_RECURSION_DEPTH:
        # Debug statement to indicate the maximum recursion depth is reached
        print("\nMaximum recursion depth reached.")
        return None

    for movie_name, recs in list(global_recommendations.items()):
        if depth <= len(recs):
            next_movie = recs[depth - 1]
            new_recs = get_recommendations(next_movie)
            add_to_global_recommendations(movie_name, new_recs)

    # Check if a common movie is found after expanding the recommendations
    common_movie = find_common_movie()
    if common_movie:
        return common_movie

    # Recursive call to continue expanding recommendations
    return recursive_search(depth + 1)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        global global_recommendations  # Use the global dictionary
        global_recommendations = {}  # Reset the global recommendations dictionary

        movies = []
        for i in range(1, 5):
            movie = request.form.get(f"movie{i}")
            if movie:
                movies.append(movie)
                initial_recs = get_recommendations(movie)
                add_to_global_recommendations(movie, initial_recs)

        # Start the recursive search for a common movie
        common_movie = recursive_search()

        if not common_movie:
            # Return a special message if no common movie is found
            common_movie = "No common movie found across all recommendations."

        return render_template("movie_map.html", movies=movies, recommendations=global_recommendations, common_movie=common_movie)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)