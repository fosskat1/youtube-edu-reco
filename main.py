import ast

from googleapiclient.discovery import build

API_VERSION = 'v3'
SERVICENAME = 'youtube'
DEVELOPER_KEY = 'AIzaSyChnpuiesF1TN1aLmylKumzL6ahB7F6WxY'

searchTerm = "Overview of " + input("Enter search term(s): \n")

# Use search term to retrieve a list of educational YouTube videos in Python dictionary format

maxResults = 1

with build(serviceName=SERVICENAME, version=API_VERSION, developerKey=DEVELOPER_KEY) as service:

    request = service.search().list(q=searchTerm, part='snippet', type='video', maxResults=maxResults)
    result = request.execute()

print(result)


# Pipe the dict-format text into a file that we can subsequently work with

with open("output_files/searchResults.txt", "w+") as file:
       file.write(str(result))


# Open the newly created text file to extract information from it

with open("output_files/searchResults.txt", "r") as file:
    contents = file.read()
    searchResults = ast.literal_eval(contents)

"""
searchResults is a text file (containing a Python dictionary in string format) that contains info on five (double-check
this #) videos. The "items" key itself contains a list of many keys, of which "id" is of interest to us. The "id" key 
contains another key called "videoId," which we can combine with the string "https://www.youtube.com/watch?v=" to give 
us the URL to the video of interest.
"""

videoInfo = searchResults["items"]

urlList = []
videoIdList = []
videoStatsTable = []
finalVideoList = []

for video in videoInfo:
    videoIdList.append(video["id"]["videoId"])
    urlList.append("https://www.youtube.com/watch?v=video" + video["id"]["videoId"])


with build(serviceName=SERVICENAME, version=API_VERSION, developerKey=DEVELOPER_KEY) as service:

    request = service.videos().list(part='statistics', id=videoIdList)
    result = request.execute()
    videoStats = result["items"]    # videoStats contains a Python list of info pertaining to each video provided in
                                    # videoIdList. Relevant info includes view count and like & dislike counts.

for video in videoStats:

    row = []
    videoStatsInfo = video["statistics"]

    if len(videoStatsInfo) < 5:
        continue
        # We want all the stats on the video. Some videos make their likes/dislikes private (I think?), so I'm opting
        # to skip these.

    videoId = video["id"]
    videoURL = "https://www.youtube.com/watch?v=video" + videoId
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
    videoStatsTable.append(row)
    # FYI: .extend() is a Python method that simultaneously appends many items to a list (rather than having to
    # individually append each item.

print(videoStatsTable)

# Code below looks through the table with all the video stats and returns the top 10 based on some engagement metrics.
# For the minimum viable product, we are only looking at the like/dislike ratio.
for video in videoStatsTable:

    videoURL = video[1]
    commentCount = video[2]
    viewCount = video[3]
    likeDislikeRatio = video[6]



print("\n\n\n#### END ####")

