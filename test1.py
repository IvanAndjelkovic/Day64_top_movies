import os
from dotenv import load_dotenv
import requests
load_dotenv()


movie_id=275625

url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

api_token= os.environ.get("API_TOKEN")




headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_token}"
}



response = requests.get(url, headers=headers)

data=response.json()
print(data["id"])
print(data["title"])
print(data["poster_path"])
print(data["overview"])
print(data["release_date"][0:4])