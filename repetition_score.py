from return_search_results import return_search_results
from googleapiclient.discovery import build


def return_video_ids(dict_of_results):
    results = dict_of_results['items']
    list_of_video_ids = []
    for video in results:
        video_info = video['id']
        video_id = video_info['videoId']
        list_of_video_ids.append(video_id)
    return list_of_video_ids


def return_list_of_caption_tracks(list_of_video_ids):
    API_VERSION = 'v3'
    SERVICENAME = 'youtube'
    DEVELOPER_KEY = 'AIzaSyChnpuiesF1TN1aLmylKumzL6ahB7F6WxY'

    list_of_caption_tracks = []

    for video_id in list_of_video_ids:
        with build(serviceName=SERVICENAME, version=API_VERSION,
                   developerKey=DEVELOPER_KEY) as service:
            request = service.captions().list(part='snippet',
                                             videoId=video_id)
            result = request.execute()
            list_of_caption_tracks.append(result)
    return list_of_caption_tracks

term = input("Enter search term(s):  \n")
dict_of_results = return_search_results(term)
list_of_video_ids = return_video_ids(dict_of_results)
list_of_caption_tracks = return_list_of_caption_tracks(list_of_video_ids)
print(list_of_caption_tracks)

