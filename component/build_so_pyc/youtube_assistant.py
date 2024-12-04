import json
import requests
import random
from urllib.parse import parse_qs, urlparse
def return_id_from_name(name):
    url = "https://push.javisco.com/api/search-song?name=" + name
    payload = {}
    headers = {}    
    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)[0]["videoId"]
    return result
def return_url_from_id(id):
    url = "https://push.javisco.com/api/youtube-parse?id=" + id

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)["url"]
    return result
    
def getVideoId(url):
    if (url.find('watch?v=') != -1):
        return parse_qs(urlparse(url).query).get("v")
    elif (url.find('youtu.be/') != -1):
        urstart_id_idex = url.find('youtu.be/') + len("youtu.be/")
        id = url[urstart_id_idex:]
        return id
    return ""

def getListId(url):
    if (url.find('watch?v=') != -1):
        list = parse_qs(urlparse(url).query).get("list")
        return list
    return ""
def return_url_from_url(url):
    id = getVideoId(url)
    return return_url_from_id(id)   
def get_id_in_playlist(play_list):
    url = "https://www.googleapis.com/youtube/v3/playlistItems?key=AIzaSyC6wShlLToYR3OgWFPBw_OaiXR6NhJlh2Y&maxResults=25&part=id%2Csnippet&playlistId=" + play_list

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    list = json.loads(response.text)["items"]
    list_playlist=[]
    for lis in list:
        list_playlist.append(lis["snippet"]["resourceId"]["videoId"])
    return list_playlist
def return_the_same_id(id, number):
    url = "https://www.youtube.com/watch?v="+id+"&pbj=1&has_verified=1"

    payload={}
    headers = {
    'x-youtube-client-version': '2.20220629.01.00',
    'x-youtube-client-name': '1',
    'Cookie': 'GPS=1; VISITOR_INFO1_LIVE=l7IkNauNy40; YSC=Y-ZKcSk456E'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    list = json.loads(response.text)[3]["response"]["contents"]["twoColumnWatchNextResults"]["secondaryResults"]["secondaryResults"]["results"]
    list_id = []
    number_list = 0
    for i in list:
        if i.get("compactVideoRenderer") != None :
            list_id.append(i["compactVideoRenderer"]["videoId"])
            number_list = number_list + 1
        if number_list == number:
            break
    return list_id