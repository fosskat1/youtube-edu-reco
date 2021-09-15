from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import logging


def return_video_transcripts(list_of_video_ids):
    transcripts = []
    for video_id in list_of_video_ids:
        try:
            transcripts.append(YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US']))
        except Exception as error:
            logging.error(error)  # log error
    return transcripts


def return_list_of_words(transcripts):
    transcripts_words = []
    for video_transcript in transcripts:
        list_of_words = []
        for dict_of_lines in video_transcript:
            stripped_line = dict_of_lines['text'].strip()
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


def return_top_n_video_ids(repetition_standardized_list, dict_count_to_id):
    repetition_standardized_list.sort(reverse=True)
    list_of_top_n_counts = repetition_standardized_list[0:5]
    list_of_top_n_video_ids = []
    for count in list_of_top_n_counts:
        list_of_top_n_video_ids.append(dict_count_to_id[count])
    return list_of_top_n_video_ids


def return_top_n_urls_from_ids(list_of_top_n_video_ids):
    url_list = []
    for id in list_of_top_n_video_ids:
        url = "https://www.youtube.com/watch?v=" + id
        url_list.append(url)
    return url_list
