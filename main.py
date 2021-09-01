from googleapiclient.discovery import build
import json

API_VERSION = 'v3'
SERVICENAME = 'youtube'
DEVELOPER_KEY = 'AIzaSyChnpuiesF1TN1aLmylKumzL6ahB7F6WxY'

searchTerm = "Overview of " + input("Enter search term(s): \n")

# Use search term to retrieve a list of educational YouTube videos in JSON format

maxResults = 3

with build(serviceName=SERVICENAME, version=API_VERSION, developerKey=DEVELOPER_KEY) as service:

    request = service.search().list(q=searchTerm, part='snippet', type='video', maxResults=maxResults)
    result = request.execute()

print(result)

# Pipe the JSON-format text into a text file that we can subsequently work with

with open("searchResults.json", "w+") as file:

    resultJsonFormat = str(result).replace("'", '"')     # Replace all single quotes with double quotes, otherwise json.load() below fails
    file.write(resultJsonFormat)


# Open the newly created JSON file to extract information from it

with open("searchResults.json", "r") as jsonFile:
    searchResults = json.load(jsonFile)

"""
searchResults is a JSON file that contains info on five (double-check this #) videos. The "items" key itself contains a 
list of many keys, of which "id" is of interest to us. The "id" key contains another key called "videoId," which we can 
combine with the string "https://www.youtube.com/watch?v=" to give us the URL to the video.
"""

videoInfo = searchResults["items"]
urlList = []

for video in videoInfo:
    urlList.append("https://www.youtube.com/watch?v=video" + video["id"]["videoId"])

print(urlList)

