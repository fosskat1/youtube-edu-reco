from engagement_metrics.VideoInfoHandler import VideoInfoHandler as VidHand
from engagement_metrics.YouTubeDataAPI import YouTubeDataAPI
from educational_metrics.repetition_score import return_video_transcripts, return_list_of_words, \
    filter_list_of_words, make_repetition_counts_list, make_dict_count_to_id, \
    return_top_n_video_ids, return_top_n_urls_from_ids

YouTubeDataAPI = YouTubeDataAPI()
quitProgram = False

while not quitProgram:

    searchTerm = YouTubeDataAPI.getSearchTerm()

    if searchTerm.lower().strip() == "q":
        print("Exiting program...")
        break

    searchRequestResult = YouTubeDataAPI.searchRequest()
    YouTubeDataAPI.storeSearchRequestResult(searchTerm, searchRequestResult)
    # Uncomment if you want to store initial (unranked) search list.

    """
    searchRequestResult is a Python dictionary that contains info on a MAX_RESULTS number of videos. The "items" key 
    itself contains a list of many keys, of which "id" is of interest to us. The "id" key contains another key called 
    "videoId," which we can combine with the string "https://www.youtube.com/watch?v=" to give us the URL to the video 
    of interest.
    """

    VidHand = VidHand(searchRequestResult)
    videoInfo = VidHand.makeVideoInfoList()
    videoIdList = VidHand.makeVideoIdList()
    videoStats = YouTubeDataAPI.getVideoStats(videoIdList)
    videoStatsList = YouTubeDataAPI.getVideoStatsList(videoStats)

    engagementRankedList = VidHand.makeSortedVideoStatList(videoStatsList, searchTerm)

    list_video_ids = [i[0] for i in engagementRankedList]

    transcripts = return_video_transcripts(list_video_ids)
    transcripts_words = return_list_of_words(transcripts)
    filtered_transcripts_words = filter_list_of_words(transcripts_words)
    repetition_standardized_list = make_repetition_counts_list(filtered_transcripts_words)
    dict_count_to_id = make_dict_count_to_id(list_video_ids,
                                         repetition_standardized_list)
    list_of_topN_video_ids = return_top_n_video_ids(
        repetition_standardized_list,
                                                 dict_count_to_id)
    topN_url_list = return_top_n_urls_from_ids(list_of_topN_video_ids)
    print(topN_url_list)

print("/n/n ### END ###")