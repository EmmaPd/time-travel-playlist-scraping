import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

CLIENT_ID = "105364dcaad64be283e27668fe8bfd20"
CLIENT_SECRET = "8e7868eaa9da41228d6b296ad84e056c"
redirect_uri = "http://example.com"
scope = "playlist-modify-public"

BILLBOARD_URL = "https://www.billboard.com/charts/hot-100"


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]

response = requests.get(f"{BILLBOARD_URL}/{date}")
billboard_webpage = response.text

# Scraped Billboard website for the hits of a date introduced by the user
soup = BeautifulSoup(billboard_webpage, "html.parser")
titles_results = soup.find_all("h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only", id="title-of-a-story")

song_titles = [song.string.strip("\n") for song in titles_results]
print(song_titles)

# Create a word, copy-paste the song titles from the prompt, delete all the quotes, and paste the result back. Needs revising
data = input("Please give me the refined data: ")

refined_song_titles = data.split(",")
print(refined_song_titles)

refined_song_title_list = [song.strip(" ") for song in refined_song_titles]
print(refined_song_title_list)

# Authenticated in Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scope=scope,
    redirect_uri=redirect_uri,
    show_dialog=True,
    cache_path="token.txt")
)

user = sp.current_user()["id"]
print(user)

# Created a list of URIs for the songs that were hits at that date
song_uris = []
for song in refined_song_title_list:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        uri = (result["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"{song} not found in Spotify.")
    else:
        song_uris.append(uri)
print(song_uris)

# Created the playlist in spotify
playlist = sp.user_playlist_create(user=user, name=f"{date} ~ Billboard 100ish", description=f"The best hits of {date} as curated by Billboard")
playlist_id = playlist["id"]

# Add songs to that playlist
tracks_added = sp.playlist_add_items(playlist_id=playlist_id, items=song_uris, position=None)
print(tracks_added)