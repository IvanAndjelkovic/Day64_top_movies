import os
from dotenv import load_dotenv
import requests
load_dotenv()


api_key = os.environ.get("API_KEY")
print(api_key)
print("mile")

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
print(response.json())

# for movie in response:
#     print (response.json())