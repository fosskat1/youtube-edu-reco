from operator import itemgetter
import csv

class VideoInfoHandler:

    def __init__(self, searchRequestResult):
        self.searchRequestResult = searchRequestResult
        self.videoIdList = []
        self.videoInfo = None
        self.engagementRankedList = []

    def makeVideoInfoList(self):
        self.videoInfo = self.searchRequestResult["items"]
        return self.videoInfo

    def makeVideoIdList(self):

        for video in self.videoInfo:
            self.videoIdList.append(video["id"]["videoId"])

        return self.videoIdList

    def makeSortedVideoStatList(self, videoStatsList, searchTerm):

        self.engagementRankedList = sorted(videoStatsList, key=itemgetter(6,3), reverse=True)

        storeFileName = ""
        numResults = len(self.engagementRankedList)
        storeFileNamePart = "_ENGAGE_RANKED_MAX_RES_" + str(numResults) + ".csv"
        searchTermList = searchTerm.lstrip().rstrip().split()

        for word in searchTermList:
            storeFileName = storeFileName + word.capitalize()

        with open(storeFileName + storeFileNamePart, 'w+', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            count = 1
            NUM_RANKED_ITEMS = 15

            for row in self.engagementRankedList:

                if count > NUM_RANKED_ITEMS:
                    break

                count += 1
                writer.writerow(row)

        return self.engagementRankedList