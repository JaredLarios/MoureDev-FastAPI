def movie_scheme(movie) -> dict:
    return {"id": str(movie["_id"]),
           "name": movie["name"],
           "image": movie["image"],
           "url": movie["url"],
           "tag": movie["tag"],
           "year": movie["year"]}