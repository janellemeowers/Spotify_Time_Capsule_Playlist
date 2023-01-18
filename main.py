import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config

date = input("Which year do you want to travel to?"
               " Type the date in this format YYYY-MM-DD:")

URL = "https://www.billboard.com/charts/hot-100/"



#authenticate spotify object, sends you to url to get token
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=config.spotify_id,
        client_secret=config.client_s,
        show_dialog=True,
        cache_path="token.txt"
    )
)

# get your own user ID
user_id = sp.current_user()["id"]

response = requests.get(URL+date)

website_html = response.text

soup = BeautifulSoup(website_html,"html.parser")

all_songs = soup.find_all(name="h3", class_="a-no-trucate")

#remove excess text
song_titles = [song.getText().strip("\n\t") for song in all_songs]

print(song_titles)

song_uris = []
year = date.split("-")[0]

for song in song_titles:
    result = sp.search(q=f"track:{song}", type="track")
    #print(result) #Prints the result
    try:
# Handling exception where the song cannot be found. It is skipped in this case.
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except IndexError:
        print(f"{song} doesn't exist in Spotify.")


# create playlist
my_playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

#add songs
sp.playlist_add_items(playlist_id=my_playlist["id"], items=song_uris)