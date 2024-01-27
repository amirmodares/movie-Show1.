import requests

API_KEY = "4696c85a8e3baedc5cabe604b9198b7e"
URL = "https://api.themoviedb.org/3/search/movie"
URL2 = "https://api.themoviedb.org/3/movie/popular?api_key=<<4696c85a8e3baedc5cabe604b9198b7e>>&language=en-US&page=1"


dic = {
    "api_key": API_KEY,
    "query": "The Matrix",
}

data = requests.get(url=URL2)
print(data.json())