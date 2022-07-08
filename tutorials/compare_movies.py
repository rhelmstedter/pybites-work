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


def compare_movies(ratings, movie1, movie2):
    if ratings[movie1] > ratings[movie2]:
        print(f"{movie1.title()} has a higher rating than {movie2.title()}.")
    else:
        print(f"{movie2.title()} has a higher rating than {movie1.title()}.")


compare_movies(movie_ratings, "star wars", "batman")
