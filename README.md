# 🎬 FilmTersection 

Welcome to the FilmTersection - the Common Movie Finder! This project stemmed from my fascination with movies and the constant struggle of finding a movie that all my friends and I can agree on watching. To solve this problem, I decided to create a flask based website that would help find a common movie recommendation based on multiple input movies. The tool uses a recursive algorithm that makes API calls to the TMDB (The Movie Database) API, searching for a movie that is common across all or most of the input movies.

<br>
<h2>The Algorithm</h2>

The FilmTersection algorithm works as follows:

	1.	Initial API Call: For each movie entered by the user, the tool makes an API call to TMDB to fetch the top 20 recommended movies.
	2.	Recursive Search: If no common movie is found across all input movies, the algorithm recursively makes API calls on the recommendations, expanding the search until a common movie is found or a predefined threshold is reached.
	3.	Best Alternative: If no common movie is found across all movies after reaching the threshold, the algorithm identifies the best alternative—a movie that is common across the maximum number of input movies.

<br>
<h2>Tech Stack</h2>

	•	Python: Core language used for backend logic.
	•	Flask: Lightweight web framework used to create the web application.
	•	TMDB API: Used to fetch movie recommendations based on user input.
	•	HTML/CSS: Used to build the front-end interface.
	•	JavaScript: Handles dynamic loading screen functionality and form submission.
	•	GitHub: Version control and project management.

<br>
<h2>Getting Started</h2>

To get started with FilmTersection:

1. Clone the repository:
 ```
git clone https://github.com/madhav1310/FilmTersection.git
cd common-movie-finder
```

2. Install the required packages:
 ```
pip install -r requirements.txt
```

3. Set up your TMDB API key:
 ```
TMDB_API_KEY=your_api_key_here
```

4. Run the application:
 ```
python app.py
```

5. Open your browser and go to http://127.0.0.1:5000 to use FilmTersection

<br>
<h2>Example Video</h2>

https://github.com/user-attachments/assets/35ca6b3c-aee5-4453-8bee-1fe0c04af08a


