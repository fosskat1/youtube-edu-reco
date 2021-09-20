from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import logging


def return_video_transcripts(list_of_video_ids):
    """
    Uses YouTubeTranscriptApi to pull transcripts from video IDs
    :param list_of_video_ids: list of unique video ids
    :return: list of lists (each inner list has one transcript per ID)
    """
    transcripts = []
    for video_id in list_of_video_ids:
        try:
            transcripts.append(YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US']))
        except Exception as error:
            logging.error(error)  # log error
    return transcripts


def return_list_of_words(transcripts):
    """
    Strips each transcript of new lines & splits transcript string into
    individual words
    :param transcripts: return from return_video_transcripts function
    :return: list of lists (each inner list has words used in each
    video)
    """
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
    """
    Removes stop words from each list of words
    :param transcripts_words: return from return_list_of_words function
    :return: list of lists (each inner list contains words excluding stopwords)
    """
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
    """
    Creates one data frame of unique words & their counts for one transcript
    :param filtered_word_list: return from filter_list_of_words function
    :return: single data frame in descending order of counts > 1
    """
    filtered_words_data = np.array(filtered_word_list)
    unique_words, counts = np.unique(filtered_words_data, return_counts=True)
    df = pd.DataFrame({'unique_words': unique_words, 'counts': counts},
                      columns=['unique_words', 'counts'])
    df_descending = df.sort_values(['counts'], ascending=[False])
    df_descending = df_descending[df_descending.counts > 1]
    return df_descending


def make_repetition_counts_list(filtered_transcripts_words):
    """
    Creates data frame for each filtered word list & determines total
    number of repetitions divided by total number of words in video.
    :param filtered_transcripts_words: return from filter_list_of_words function
    :return: list of standardized repetition counts per video
    """
    repetition_standardized_list = []
    for filtered_list in filtered_transcripts_words:
        df = return_data_frame(filtered_list)
        counts_each_word = list(df["counts"])
        repetition_count = sum(counts_each_word)
        repetition_count_standardized = repetition_count / len(filtered_list)
        repetition_standardized_list.append(repetition_count_standardized)
    return repetition_standardized_list


def make_dict_count_to_id(list_video_ids, repetition_standardized_list):
    """
    Zips list of video ids with repetition scores to create dictionary
    :param list_video_ids: pulled from search results using YouTube Data API
    :param repetition_standardized_list: return from make_repetition_counts_list
    :return: returns dictionary with count as key & id as value. If key is
    the same for two videos, one will get overwritten.
    """
    dict_count_to_id = dict(zip(repetition_standardized_list, list_video_ids))
    return dict_count_to_id


def return_top_n_video_ids(repetition_standardized_list, dict_count_to_id):
    """
    Uses dictionary to pull ID using keys from sorted repetition scores list
    :param repetition_standardized_list: list of repetition scores to be
    sorted in function
    :param dict_count_to_id: dictionary of repetition scores to video IDs
    :return: list of top 5 results based on score
    """
    repetition_standardized_list.sort(reverse=True)
    list_of_top_n_counts = repetition_standardized_list[0:5]
    list_of_top_n_video_ids = []
    for count in list_of_top_n_counts:
        list_of_top_n_video_ids.append(dict_count_to_id[count])
    return list_of_top_n_video_ids


def return_top_n_urls_from_ids(list_of_top_n_video_ids):
    """
    Appends video ID to link to create full URL
    :param list_of_top_n_video_ids: return from return_top_n_video_ids function
    :return: list of youtube urls from top N results
    """
    url_list = []
    for id in list_of_top_n_video_ids:
        url = "https://www.youtube.com/watch?v=" + id
        url_list.append(url)
    return url_list
