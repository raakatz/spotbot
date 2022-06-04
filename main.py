import time
import praw
import os
import requests
import json
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import pprint

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

reddit_titles = list()
song_uris = list()

reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
        )

subreddit = reddit.subreddit('progmetal')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='playlist-modify-public'))


for submission in subreddit.top(limit=None,time_filter='day'):
    if not submission.is_self and ('youtube.com' in submission.url or 'youtu.be' in submission.url):
        reddit_titles.append(re.sub('[\(\[].*?[\)\]]', '', submission.title))
    elif not submission.is_self and 'open.spotify.com' in submission.url:
        spotify_id_regex = re.compile(r'track/(.*)\?')
        track_id = spotify_id_regex.search(submission.url)
        song_uris.append(sp.track(track_id.group(1))['uri'])

for song in reddit_titles:
    try:
        result = sp.search(song,limit=1)
        song_uris.append(result['tracks']['items'][0]['uri'])
        time.sleep(2)
    except:
        try:
            result = sp.search(song,limit=1)
            song_uris.append(result['tracks']['items'][0]['uri'])
            time.sleep(2)
        except:
            pass

sp.playlist_add_items('3TnbT8juRWLXxkHEDZtGlO', song_uris)
