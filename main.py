from googleapiclient.discovery import build

API_VERSION = 'v3'
SERVICENAME = 'youtube'
DEVELOPER_KEY = 'AIzaSyChnpuiesF1TN1aLmylKumzL6ahB7F6WxY'

searchTerm = input("Enter search term(s):  \n")

with build(servicename=SERVICENAME, version=API_VERSION, developerKey=DEVELOPER_KEY) as service:
    request = service.search().list(q=searchTerm, part='snippet', type='video')
    result = request.execute()
    
print(result)
