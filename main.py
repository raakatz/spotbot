import time
import pprint
import praw
import os
import requests
import json
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')
GOOGLE_API = os.getenv('GOOGLE_API')
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

video_ids = list()
reddit_titles = list()
youtube_titles = list()
song_uris = list()

reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
        )

subreddit = reddit.subreddit('progmetal')



def check_if_ffo(listed_title):
    for word in listed_title:
        if 'FFO' in word:
            return listed_title.index(word)

for submission in subreddit.top(limit=None,time_filter='day'):
    if not submission.is_self:
        # GET URL FOR YOUTUBE QUERY
        if 'youtube.com' in submission.url:
            id = submission.url.split('=')
            video_ids.append(id[-1])
        elif 'youtu.be' in submission.url:
            id = submission.url.split('/')
            video_ids.append(id[-1])
        # GET REDDIT TITLE WITHOUT FFO
        title = submission.title.split()
        if check_if_ffo(title) != None:
            index = check_if_ffo(title)
            try:
                while True:
                    title.pop(index)
            except IndexError:
                pass
        reddit_titles.append(title)

# BUILD QUERY FROM YOUTUBE TITLES

youtube_params = {'key': GOOGLE_API, 'part': 'snippet', 'id': ','.join(video_ids)}

youtube_r = requests.get('https://youtube.googleapis.com/youtube/v3/videos', params=youtube_params)

forbidden_names = ['official', 'video', 'audio', 'visualizer', 'music']

for item in youtube_r.json()['items']:
    title = item['snippet']['title'].lower().split()
    for forbidden in forbidden_names:
        for word in title:
            if forbidden in word:
                title.remove(word)
    youtube_titles.append(title)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='playlist-modify-public'))



for song in reddit_titles:
    q = ' '.join(song)
    try:
        result = sp.search(q,limit=1)
        song_uris.append(result['tracks']['items'][0]['uri'])
        time.sleep(2)
    except:
        try:
            result = sp.search(q,limit=1)
            song_uris.append(result['tracks']['items'][0]['uri'])
            time.sleep(2)
        except:
            pass

sp.playlist_add_items('3TnbT8juRWLXxkHEDZtGlO', song_uris)
