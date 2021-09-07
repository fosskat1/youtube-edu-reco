from googleapiclient.discovery import build


def return_search_results(search_term):
    API_VERSION = 'v3'
    SERVICENAME = 'youtube'
    DEVELOPER_KEY = 'AIzaSyChnpuiesF1TN1aLmylKumzL6ahB7F6WxY'
    with build(serviceName=SERVICENAME, version=API_VERSION,
               developerKey=DEVELOPER_KEY) as service:
        request = service.search().list(q=search_term, part='snippet',
                                        type='video')
    result = request.execute()
    return result


term = input("Enter search term(s):  \n")
dict_of_results = return_search_results(term)
print(dict_of_results)
