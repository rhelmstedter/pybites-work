movies = [
    "star wars",
    "the batman",
    "the dark knight",
    "rush hour",
    "blues brothers",
    "ocean's eleven",
    "shaft",
    "back to the future",
]

movies.remove("the batman")
movies.append("batman")

static_movies = tuple(movies)
print("The possible movies are:")
for movie in static_movies:
    print(f"+ {movie.title()}")
