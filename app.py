from flask import Flask, render_template, request
import requests

TMDB_API_KEY = "f4484338cde529648772ad772863c20c"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        movie = request.form["movie"]

        print(f"You searched for {movie}") ##remove
        return recommend_movies(movie)
    return render_template("index.html")

def recommend_movies(movie):
    api_key = TMDB_API_KEY
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie}"
    response = requests.get(search_url).json()
    
    if response["results"]:
        movie_id = response["results"][0]["id"]
        recommendations_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={api_key}"
        recommendations = requests.get(recommendations_url).json()["results"]
        recommendations = [i["title"] for i in recommendations]

        print(recommendations)
        
        return render_template("movie_map.html", movie=movie, recommendations=recommendations)
    else:
        return render_template("index.html", error="Movie not found.")
        

if __name__ == "__main__":
    app.run(debug=True)