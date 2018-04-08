import requests
from collections import namedtuple

#Simple comparing between two dates in following string format: 'yyyy-mm-dd'
def is_older_date(first_date, second_date):
    for i in range(len(first_date)):
        if first_date[i] < second_date[i]: return True
        elif first_date[i] > second_date[i]: break

    return False

#Checking if date is in our range
def is_date_in_range(date, dates_range):
    if is_older_date(date, dates_range.start): return False
    if is_older_date(dates_range.end, date): return False

    return True

def gather_channel_videos(channel_id, page_token=''):
    #Preparing API Call URL
    api_call = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={channel_id}&key={API_KEY}'
    if page_token != '': api_call = api_call + f'&pageToken={page_token}'

    #Output container
    gathered_videos = []

    #Making call & parsing output
    r = requests.get(api_call)
    call_output = r.json()

    items = call_output['items']

    for upload in items:
        snippet = upload['snippet']
        gathered_videos.append(Video(title=snippet['title'], id=snippet['resourceId']['videoId'],
                                     date=snippet['publishedAt'].split('T', 1)[0]))

    #Gathering further until the end
    try:
        page_token = call_output['nextPageToken']
        gathered_videos.extend(gather_channel_videos(channel_id, page_token))
    except KeyError:
        pass
    
    return gathered_videos

#Basic API Call data
API_KEY = 'AIzaSyBI7omQ3Wja1wVMNfVwJbwUh4agH34D56Y'
channel_id = 'UUJHA_jMfCvEnv-3kRjTCQXw' #Binging with Babish

#Preparing containers
Video = namedtuple('Video', 'title id date')
videos = gather_channel_videos(channel_id)

#Sorting aquired data by date
sorted(videos, key=lambda x:x.date)

#Setting up data range
DateRange = namedtuple('DateRange', 'start end')
date_range = DateRange('2018-01-01', '2018-03-03')

#Removing videos out of our date range
videos = [v for v in videos if is_date_in_range(v.date, date_range)]

for v in videos: 
    print(f'{v.title}-{v.date}')