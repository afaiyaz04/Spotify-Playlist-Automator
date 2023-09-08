from dotenv import load_dotenv
import os
import base64
import requests
import json
import urllib


class SpotifyClient(object):
    def __init__(self):
        self.api_token = self.get_api_token()

    def get_api_token(self):
        # .env needs to be created with CLIENT_ID & CLIENT_SECRET
        load_dotenv()
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        auth_string = client_id + ":" + client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = requests.post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token

    def search_songs(self, artist, track):
        query = urllib.parse.quote(f"{artist} {track}")
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(
            url,
            headers={
                "content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )
        response_json = response.json()
        results = response_json['track']['items']
        if results:
            return results[0]['id']
        else:
            raise Exception(f"No song found for {artist} = {track}")

    def add_songs_to_spotify(self, song_id):
        url = "https://api.spotify.com/v1/me/tracks"
        response = requests.put(
            url,
            json ={
                "ids":[song_id]
            },
            headers={
                "content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )
        return response.ok
