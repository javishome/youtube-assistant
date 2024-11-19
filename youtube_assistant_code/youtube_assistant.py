import json
import requests
import random
from urllib.parse import parse_qs, urlparse
import socket
import time
def get_local_ip():
    try:
        # Kết nối tạm thời để lấy địa chỉ IP cục bộ
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Kết nối đến một địa chỉ ngoài để nhận IP cục bộ
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip
    
def return_id_from_name(name):
    url = "https://push.javisco.com/api/search-song?name=" + name
    payload = {}
    headers = {}    
    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)[0]["videoId"]
    return result
def return_url_from_id(id, entity):
    timestamp = str(int(time.time()))
    entity = entity.replace("media_player.", "")
    url = 'http://' + get_local_ip() + ':2024/stream/' + entity + "/" + id +'.flac' + "?ts=" + timestamp
    return url
    
def getVideoId(url):
    if (url.find('watch?v=') != -1):
        return parse_qs(urlparse(url).query).get("v")
    elif (url.find('youtu.be/') != -1):
        urstart_id_idex = url.find('youtu.be/') + len("youtu.be/")
        id = url[urstart_id_idex:]
        return id
    return ""
    
def return_url_from_id_javis(id):
    url = "https://push.javisco.com/api/youtube-parse?id=" + id

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)["url"]
    return result
    
def getListId(url):
    if (url.find('watch?v=') != -1):
        list = parse_qs(urlparse(url).query).get("list")
        return list
    return ""
# def return_url_from_url(url, entity):
#     id = getVideoId(url)
#     return return_url_from_id(id, entity)   
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

    list = json.loads(response.text)["response"]["contents"]["twoColumnWatchNextResults"]["secondaryResults"]["secondaryResults"]["results"]
    list_id = []
    number_list = 0
    for i in list:
        if i.get("compactVideoRenderer") != None :
            list_id.append(i["compactVideoRenderer"]["videoId"])
            number_list = number_list + 1
        if number_list == number:
            break
    return list_id