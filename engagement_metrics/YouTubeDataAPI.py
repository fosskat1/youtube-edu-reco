from constants import Constants
from googleapiclient.discovery import build


# This class handles everything related to the YouTube Data API. It contains a function that prompts the user for a topic
# that they would like to learn about and then completes a search request with the API. This class also deals with
# retrieving video stats (e.g., likes & dislikes) to be used as our engagement metrics.
class YouTubeDataAPI:
    API_VERSION = Constants.GOOGLE_CLOUD_API_VERSION
    SERVICE_NAME = Constants.GOOGLE_CLOUD_SERVICE_NAME
    DEVELOPER_KEY = Constants.GOOGLE_CLOUD_API_KEY
    MAX_RESULTS = 20

    def __init__(self):

        self.searchTerm = None
        self.relatedTermsList = []
        self.videoStats = None
        self.videoStatsTable = []

    # Prompt user for topic that they want to learn about.
    def getSearchTerm(self):
        searchTerm = self.searchTerm = "Learn about " + input("Enter search term [q: quit]: \n")
        return searchTerm

    # After receiving the initial search term, compile a list of related terms to add to the playlist.
    # Doesn't have full functionality yet. Need to implement method to automatically compile a list of
    # related topics (i.e., user doesn't need to manually supply the list of topics).
    def getRelatedSearchTerms(self):
        proceed = False
        input_mode = None
        while not proceed:
            input_mode = input("Manual or comma-separated file input [manual/file]? \n").strip().lower()

            if input_mode not in ["manual", "file"]:
                print("Error: invalid input. Try again. ")

            else:
                proceed = True

        if input_mode == "manual":
            cond = ""

            while not cond == "q":
                relatedTerm = input("Type out related term [q: quit] \n")

                if relatedTerm.lower().strip() == "q":
                    cond = "q"

                else:
                    self.relatedTermsList.append(relatedTerm)

        if input_mode == "file":

            fileName = input("Name of file with related terms (include extension)? \n")

            with open(fileName, "r") as file:
                contents = file.readlines()
                self.relatedTermsList = contents[0].split(",")

        return self.relatedTermsList

    # Completes a search request with the API to return a list of videos using the supplied search term.
    def searchRequest(self):

        with build(serviceName=self.SERVICE_NAME, version=self.API_VERSION, developerKey=self.DEVELOPER_KEY) as service:

            request = service.search().list(q=self.searchTerm, part='snippet', type='video', maxResults=self.MAX_RESULTS)
            result = request.execute()
            return result

    # Stores the result of the search request in a file for viewing after the program termiantes.
    def storeSearchRequestResult(self, searchTerm, searchRequestResult):

        storeFileName = ""
        storeFileNamePart = "_MAX_RES_"
        searchTermList = searchTerm.lstrip().rstrip().split()

        for word in searchTermList:
            storeFileName = f"{storeFileName} + {word.capitalize()}.txt"

        with open("output_files/" + storeFileName + storeFileNamePart + str(self.MAX_RESULTS), "w+") as file:
            file.write(str(searchRequestResult))

    # Returns a list of videos corresponding to the search term. List contains stats on the video, like
    # view count, like/dislike count, like/dislike ratio and comment count.
    def getVideoStats(self, videoIdList):

        with build(serviceName=self.SERVICE_NAME, version=self.API_VERSION, developerKey=self.DEVELOPER_KEY) as service:

            request = service.videos().list(part='statistics', id=videoIdList)
            result = request.execute()
            self.videoStats = result["items"]    # videoStats is a Python list of stats pertaining to each video provided in
                                                 # videoIdList. Relevant info includes view count and like & dislike counts.
            return self.videoStats

    def getVideoStatsList(self, videoStats):

        for video in videoStats:
            row = []
            videoStatsInfo = video["statistics"]

            if len(videoStatsInfo) < 5:
                continue
                # We want all the stats on the video. Some videos make their likes/dislikes private (I think?), so I'm
                # opting to skip these.

            else:

                videoId = video["id"]
                videoURL = "https://www.youtube.com/watch?v=" + videoId
                commentCount = int(videoStatsInfo["commentCount"])
                viewCount = int(videoStatsInfo["viewCount"])
                likeCount = int(videoStatsInfo["likeCount"])
                dislikeCount = int(videoStatsInfo["dislikeCount"])

                try:
                    likeDislikeRatio = likeCount / dislikeCount

                except ZeroDivisionError as e:
                    print("### ERROR: " + str(e) + ". There are 0 dislikes on this video.")
                    likeDislikeRatio = "Infinite"

                try:
                    likePercent = likeCount / (likeCount + dislikeCount)

                except ZeroDivisionError as e:
                    print("ERROR: " + str(e) + ". There are 0 likes and dislikes on this video.")
                    likePercent = "Indeterminate"

                row.extend((videoId, videoURL, commentCount, viewCount, likeCount, dislikeCount, likeDislikeRatio, likePercent))
                self.videoStatsTable.append(row)
                # FYI: .extend() is a Python method that simultaneously appends many items to a list (rather than having to
                # individually append each item.

        return self.videoStatsTable

