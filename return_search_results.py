from VideoInfoHandler import VideoInfoHandler as VidHand
from YouTubeDataAPI import YouTubeDataAPI

YouTubeDataAPI = YouTubeDataAPI()
quitProgram = False

while not quitProgram:

    searchTerm = YouTubeDataAPI.getSearchTerm()

    if searchTerm.lower().strip() == "q":
        print("Exiting program...")
        break

    searchRequestResult = YouTubeDataAPI.searchRequest()
    print(type(searchRequestResult))
    YouTubeDataAPI.storeSearchRequestResult(searchTerm, searchRequestResult)

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

    #relatedTermsList = YouTubeDataAPI.getRelatedSearchTerms()


