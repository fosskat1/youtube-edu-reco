from googleapiclient.discovery import build

searchTerm = input("Enter search term(s)... \n")

with build('youtube', 'v3', developerKey='AIzaSyChnpuiesF1TN1aLmylKumzL6ahB7F6WxY') as service:
    request = service.search().list(q=searchTerm, part='snippet', type='video')
    result = request.execute()
    
print(result)