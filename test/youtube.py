# BUILD QUERY FROM YOUTUBE TITLES
youtube_titles = list()
video_ids = list()

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


if 'youtube.com' in submission.url:
    id = submission.url.split('=')
    video_ids.append(id[-1])
elif 'youtu.be' in submission.url:
    id = submission.url.split('/')
    video_ids.append(id[-1])
