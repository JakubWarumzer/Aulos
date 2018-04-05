import requests
from collections import namedtuple

#Basic API Call data
API_KEY = 'AIzaSyBI7omQ3Wja1wVMNfVwJbwUh4agH34D56Y'
channel_id = 'UUJHA_jMfCvEnv-3kRjTCQXw' #Binging with Babish
page_token = ''
base_playlists_call = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=UUJHA_jMfCvEnv-3kRjTCQXw&key={API_KEY}'

#Preparing containers
Video = namedtuple('Video', 'title id date')
videos = []

#Loop used to extract video data from channel
playlist_call = base_playlists_call
while True:
    r = requests.get(playlist_call)
    call_output = r.json()

    items = call_output['items']

    for upload in items:
        snippet = upload['snippet']
        videos.append(Video(title=snippet['title'], id=snippet['resourceId']['videoId'], date=snippet['publishedAt'].split('T', 1)[0]))

    try:
        page_token = call_output['nextPageToken']
    except KeyError:
        break    

    playlist_call = base_playlists_call + f'&pageToken={page_token}'

#Sorting aquired data by date
sorted(videos, key=lambda x:x.date)
