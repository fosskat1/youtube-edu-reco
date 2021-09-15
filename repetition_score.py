from return_search_results import return_search_results
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

API_VERSION = 'v3'
SERVICENAME = 'youtube'
DEVELOPER_KEY = 'AIzaSyBJiIF6-PXhzyfLVJRBseLGZXvc34vPbPY'


def return_video_ids(dict_of_results):
    results = dict_of_results['items']
    list_of_video_ids = []
    for video in results:
        video_info = video['id']
        video_id = video_info['videoId']
        list_of_video_ids.append(video_id)
    return list_of_video_ids


def return_video_transcripts(list_of_video_ids):
    transcripts = []
    for video_id in list_of_video_ids:
        try:
            transcripts.append(YouTubeTranscriptApi.get_transcript(video_id,languages=['en', 'en-US']))
        except:
            pass
    return transcripts

def return_list_of_words(transcripts):
    transcripts_words = []
    for video_transcript in transcripts:
        list_of_words = []
        for dict_of_lines in video_transcript:
            stripped_line = dict_of_lines['text'].strip()
            # tokenizer = RegexpTokenizer(r'\w+')
            # words_in_line = tokenizer.tokenize(stripped_line)
            words_in_line = stripped_line.split()
            for word in words_in_line:
                if not(("[" in word) and ("]" in word)):
                    list_of_words.append(word.lower())
        transcripts_words.append(list_of_words)
    return transcripts_words

def filter_list_of_words(transcripts_words):
    filtered_transcripts_words = []
    for transcript in transcripts_words:
        filtered_word_list = []
        for word in transcript:
            if word not in stopwords.words('english'):
                filtered_word_list.append(word)
        if len(filtered_word_list) > 0:
            filtered_transcripts_words.append(filtered_word_list)
    return filtered_transcripts_words

def return_data_frame(filtered_word_list):
    filtered_words_data = np.array(filtered_word_list)
    unique_words, counts = np.unique(filtered_words_data, return_counts=True)
    df = pd.DataFrame({'unique_words': unique_words, 'counts': counts},
                      columns=['unique_words', 'counts'])
    df_descending = df.sort_values(['counts'], ascending=[False])
    df_descending = df_descending[df_descending.counts > 1]
    return df_descending

def make_repetition_counts_list(filtered_transcripts_words):
    repetition_standardized_list = []
    for filtered_list in filtered_transcripts_words:
        df = return_data_frame(filtered_list)
        counts_each_word = list(df["counts"])
        repetition_count = sum(counts_each_word)
        repetition_count_standardized = repetition_count / len(filtered_list)
        repetition_standardized_list.append(repetition_count_standardized)
    return repetition_standardized_list

def make_dict_count_to_id(list_video_ids, repetition_standardized_list):
    dict_count_to_id = dict(zip(repetition_standardized_list, list_video_ids))
    return dict_count_to_id

def return_top10_video_ids(repetition_standardized_list, dict_count_to_id):
    repetition_standardized_list.sort(reverse=True)
    list_of_top10_counts = repetition_standardized_list[0:10]
    list_of_top10_video_ids = []
    for count in list_of_top10_counts:
        list_of_top10_video_ids.append(dict_count_to_id[count])
    return list_of_top10_video_ids;

def return_top10_urls_from_ids(list_of_top10_video_ids):
    url_list = []
    for id in list_of_top10_video_ids:
        url = "https://www.youtube.com/watch?v=" + id
        url_list.append(url)
    return url_list

term = input("Enter search term(s):  \n")
dict_of_results = return_search_results(term)
list_video_ids = return_video_ids(dict_of_results)
transcripts = return_video_transcripts(list_video_ids)
transcripts_words = return_list_of_words(transcripts)
filtered_transcripts_words = filter_list_of_words(transcripts_words)
repetition_standardized_list = make_repetition_counts_list(
    filtered_transcripts_words)
print(repetition_standardized_list)
dict_count_to_id = make_dict_count_to_id(list_video_ids,
                                    repetition_standardized_list)
list_of_top10_video_ids = return_top10_video_ids(repetition_standardized_list,
                                               dict_count_to_id)
top10_url_list = return_top10_urls_from_ids(list_of_top10_video_ids)
print(top10_url_list)



# def return_list_of_caption_tracks(list_of_video_ids):
#     list_of_caption_tracks = []
#
#     for video_id in list_of_video_ids:
#         with build(serviceName=SERVICENAME, version=API_VERSION,
#                    developerKey=DEVELOPER_KEY) as service:
#             request = service.captions().list(part='snippet',
#                                               videoId=video_id)
#             result = request.execute()
#             list_of_caption_tracks.append(result)
#     return list_of_caption_tracks
#
#
# def download_caption_track(caption_track_id):
#     with build(serviceName=SERVICENAME, version=API_VERSION,
#                developerKey=DEVELOPER_KEY) as service:
#         request = service.captions().download(id=caption_track_id)
#         result = request.execute()
#         print(result)


# term = input("Enter search term(s):  \n")
# dict_of_results = return_search_results(term)
# list_of_video_ids = return_video_ids(dict_of_results)
# list_of_caption_tracks = return_list_of_caption_tracks(list_of_video_ids)
# print(list_of_caption_tracks)
# download_caption_track('yhrevS0CbxYAIENAb3tB3zKciq4IYFLl16EUz7HrISo=')
