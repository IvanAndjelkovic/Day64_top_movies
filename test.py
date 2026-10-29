import os
from dotenv import load_dotenv
import requests
load_dotenv()



api_key = os.environ.get("API_KEY")



url = "https://api.themoviedb.org/3/search/movie"

headers = {"accept": "application/json"}
params={
    "api_key": api_key, 
    "query":"Inception",
    "include_adult": False,
    "language": "en-US",
    "page":1

}

response = requests.get(url, headers=headers, params=params)

data=response.json()


movie_data=data["results"]
for movie in movie_data:
    print(f"{movie["title"]} - {movie["release_date"]} - {movie["id"]}")