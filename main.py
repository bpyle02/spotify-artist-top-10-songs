"""

This program was written by Brandon Pyle

"""


from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

# Loads the .env file
load_dotenv()

# Gets the values from the .env values and assign them to the following variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# This function gets the authentication token to enable Spotify API access
def get_token():
    auth_string = client_id + ":" + client_secret # Creates a variable that combines the ID and Secret
    auth_bytes = auth_string.encode("utf-8") # Encode the auth string in UTF-8 to allow for base 64 encoding
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") # Encodes the string in base 64 for use in authorizing Spotify API access

    url = "https://accounts.spotify.com/api/token" # Spotify API URL

    # Headers used to access the API
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"} # Extra data to grant basic access to Spotify API

    result = post(url, headers=headers, data=data) # Sends a post request to the API to get authentication
    
    json_result = json.loads(result.content) # Loads the resulting data as a json string value
    token = json_result["access_token"] # Sets the access token from the json string to the token variable for later use
    return token # Return the token variable

# This function returns the authentication header for the API for easy access later
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# This function searches Spotify for artists based on the user's input
def search_for_artist(token, artist_name):
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1" # Spotify API query to search for the artist
    headers = get_auth_header(token) # Gets the headers to confirm authentication
    
    result = get(url, headers=headers) # Sends a get request to get the resulting data from the query
    json_result = json.loads(result.content)["artists"]["items"] # Gets the artist data in the form of a json string from the get request

    # If the result is empty, then no artist matches the search
    if len(json_result) == 0:
        print("No artist with this name exists")
        return None
    
    return json_result[0] # Return the resulting srtist data

# This function gets the top songs from the artist search for
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US" # Spotify API query to get the artist's top tracks
    headers = get_auth_header(token) # Gets the headers to confirm authentication

    result = get(url, headers=headers) # Sends a get request to get the resulting data from the query
    json_result = json.loads(result.content)["tracks"] # Gets the song data in the form of a json string from the get request

    return json_result

token = get_token() #Gets the authentication token

artist = input("Type an artist name to get their top 10 songs: ") 

result = search_for_artist(token, artist)
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

# For loop to print out the rank, song name, explicit indicator, duration, and poularity of each song
for i, song in enumerate(songs):
    minutes = int(song['duration_ms'] / 60000)
    seconds = int(((song['duration_ms'] / 60000) - minutes) * 60)
    if (song['explicit']):
        print(f"{i + 1}. {song['name']} [E] | Duration: {minutes}:{seconds} Popularity: {song['popularity']}")
    print(f"{i + 1}. {song['name']} | Duration: {minutes}:{seconds} Popularity: {song['popularity']}")