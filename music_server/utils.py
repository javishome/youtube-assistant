import json
import requests
from urllib.parse import parse_qs, urlparse
import socket
import time
import os
import yaml
from pytubefix import YouTube
from const import MODE, TOKEN_DEV, HOST_DEV, ROOT_DIR_PROD, SERVER_STREAM_DEV, ENABLE_LOG
import re
from logging import getLogger
logger = getLogger(__name__)


def get_song_id(media_content_id):
    if "https://push.javisco.com/api/youtube" in media_content_id:
        return media_content_id.split("/")[-2]
    match = re.search(r'/([^/]+)\.flac', media_content_id)
    if match:
        song_id = match.group(1)
        return song_id
    return ""
    
def get_local_ip():
    try:
        # Kết nối tạm thời để lấy địa chỉ IP cục bộ
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Kết nối đến một địa chỉ ngoài để nhận IP cục bộ
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip

def get_url_from_song_name(song_id,url,name, entity, version):
    id = ""
    if (song_id != ""):
        id = song_id
    elif (url != ""):
        id = getVideoId(url)[0]
    else: 
        id = return_id_from_name(name)
    song_url = return_url_from_id(id, entity, version)  
    return song_url 

def return_id_from_name(name):
    url = "https://push.javisco.com/api/search-song?name=" + name
    payload = {}
    headers = {}    
    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)[0]["videoId"]
    return result

def getVideoId(url):
    if (url.find('watch?v=') != -1):
        return parse_qs(urlparse(url).query).get("v")
    elif (url.find('youtu.be/') != -1):
        urstart_id_idex = url.find('youtu.be/') + len("youtu.be/")
        id = url[urstart_id_idex:]
        return id
    return ""

def return_url_from_id(id, entity, version):
    timestamp = str(int(time.time()))
    entity = entity.replace("media_player.", "")
    if version == 1:
        url = return_url_from_id_javis(id)
    else:
        if MODE == 'dev':
            url = get_server_stream() + '/stream/' + entity + "/" + id +'.flac' + "?ts=" + timestamp
        else:
            url = 'http://' + get_local_ip() + ':2024/stream/' + entity + "/" + id +'.flac' + "?ts=" + timestamp
    return url

def return_url_from_id_javis(id):
    url = "https://push.javisco.com/api/youtube-parse?id=" + id

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)["url"]
    return result

def return_url_from_id_javis_v2(id):
    url = "https://push.javisco.com/api/v2/youtube-parse?id=" + id

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)
    url = result.get("url")
    length = int(result.get("length"))
    return url, length

def get_local_host():
    if MODE == 'dev':
        return HOST_DEV
    return 'http://' + get_local_ip() + ':8123'

def call_play(media_id, media_content_id):
    song_id = get_song_id(media_content_id)
    url_youtube = "https://www.youtube.com/watch?v=" + song_id
    yt = YouTube(url_youtube)
    duration = yt.length
    service_data = get_service_play(media_id, media_content_id, yt.thumbnail_url, yt.title)
    endpoint = '/api/services/media_player/play_media'
    call_service(endpoint, service_data)
    return duration

def call_service(endpoint, data):
    host = get_local_host()
    url = f'{host}{endpoint}'
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        i = 0
        while i < 3:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                break
            time.sleep(1)
            i += 1
    except:
        write_log("error: call service")
        

def get_state(entity_id):
    host = get_local_host()
    url = f'{host}/api/states/{entity_id}'
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(url, headers=headers)
        return response.json().get('state')
    except:
        write_log("error: get state")
        return "error"


def get_token():
    if MODE == 'dev':
        return TOKEN_DEV
    secret_file = os.path.join(ROOT_DIR_PROD, 'secrets.yaml')
    data = yaml2dict(secret_file)
    return data.get('token')

def yaml2dict(filename):
    try:
        exist = os.path.exists(filename)
        if not exist:
            f = open(filename, 'w+')
            f.close()
        file = open(filename, 'r', encoding='utf8')
        res = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        return res
    except:
        return {}
    
def get_service_play(media_id, media_content_id, thumbnail_url, title):
    service_data = {
                'entity_id': media_id,
                'media_content_id': media_content_id,
                'media_content_type': 'music',
                "extra": {
                    "thumb": thumbnail_url,
                    "title": title
                    }
            }
    return service_data

def get_playlist_play(repeat, number, media_id, name, url, song_id, version):
    list_playlist = []
    song_url = get_url_from_song_name(song_id, url, name, media_id, version)
    if repeat:
        if number != 0:
            list_playlist = [song_url] * number
    else:
        list_id = return_the_same_id(song_id, number)
        list_playlist  = [return_url_from_id(id, media_id, version) for id in list_id]
    return list_playlist

def get_playlist_from_id_url(list_id, url, media_id, version):
    id=''
    if (list_id != ""):
        id = list_id
    else:
        id = getListId(url)[0]
    list_id = get_id_in_playlist(id)
    list_playlist = [return_url_from_id(id, media_id, version) for id in list_id]
    return list_playlist

def getListId(url):
    if (url.find('watch?v=') != -1):
        list = parse_qs(urlparse(url).query).get("list")
        return list
    return ""

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

def write_log(msg):
    if not ENABLE_LOG:
        return
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    file = open("log.log", "a")
    file.write(current_time + ": " + msg + "\n")
    file.close()

def get_server_stream():
    if MODE == 'dev':
        return SERVER_STREAM_DEV
    return get_local_host()

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