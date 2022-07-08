movies = []


print(f"Truthiness of movies list: {bool(movies)} ")

if movies:
    print(f"There are {len(movies)} movies to choose from.")
else:
    print("So sad, there is nothing to watch.")
