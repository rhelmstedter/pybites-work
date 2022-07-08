movie_ratings = {
    "star wars": 8.6,
    "batman": 7.5,
    "the dark knight": 9.0,
    "rush hour": 7.0,
    "blues brothers": 7.9,
    "ocean's eleven": 7.7,
    "shaft": 6.0,
    "back to the future": 8.5,
}

for movie, rating in movie_ratings.items():
    print(f"{movie.title()} has a rating of {rating}.")
