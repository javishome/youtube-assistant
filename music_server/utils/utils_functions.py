import json
import requests
from urllib.parse import parse_qs, urlparse
import socket
import time
import os
import yaml
from const import MODE, TOKEN_DEV, HOST_DEV, ROOT_DIR_PROD, SERVER_STREAM_DEV, ENABLE_LOG, YTM_DOMAIN
import re
from logging import getLogger
import json
import yt_dlp
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

def get_song_id(song_id, url):
    if song_id != "":
        return song_id
    elif url != "":
        return getVideoId(url)[0]
    return ""

def return_list_song_id_from_name(name, number):
    url = "https://push.javisco.com/api/search-song?name=" + name
    payload = {}
    headers = {}    
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        logger.error(f"Error fetching song list for name {name}: {response.status_code} - {response.text}")
        return []
    list_info = json.loads(response.text)
    if number < len(list_info):
        list_info = list_info[:number]
    list_song_id = []
    for i in list_info:
        list_song_id.append(i["videoId"])
    return list_song_id

def getVideoId(url):
    if (url.find('watch?v=') != -1):
        return parse_qs(urlparse(url).query).get("v")
    elif (url.find('youtu.be/') != -1):
        urstart_id_idex = url.find('youtu.be/') + len("youtu.be/")
        id = url[urstart_id_idex:]
        return id
    return ""

def return_song_info_from_id(media_id, id, version, name = ""):
    song_info = {}
    song_info["name"] = name
    song_info["id"] = id
    song_info["version"] = version
    if version == 1:
        url, length = return_song_info_from_id_javis(id)
        song_info["url"] = url
        song_info["length"] = length
        return song_info
    else:
        if MODE == 'dev':
            song_info["url"] = get_server_stream() + '/stream?media_id=' + media_id + '&song_id=' + id
        else:
            song_info["url"] = 'http://' + get_local_ip() + ':2024/stream?media_id=' + media_id + '&song_id=' + id
    return song_info

def return_song_info_from_id_javis(id):
    url = "https://push.javisco.com/api/v2/youtube-parse?id=" + id
    payload = {}
    headers = {}
    
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        logger.error(f"Error fetching song info for ID {id}: {response.status_code} - {response.text}")
        return "", 0
    result = json.loads(response.text)
    url, length = result.get("url"), int(result.get("length"))
    length = int(length/1000)
    return url, length

def get_local_host():
    if MODE == 'dev':
        return HOST_DEV
    return 'http://' + get_local_ip() + ':8123'

def call_play(media_id, media_content_id, name):
    service_data = get_service_play(media_id, media_content_id, name)
    endpoint = '/api/services/media_player/play_media'
    call_service(endpoint, service_data)

def call_stop(media_id):
    service_data = {
        'entity_id': media_id
    }
    endpoint = '/api/services/media_player/media_stop'
    call_service(endpoint, service_data)

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
        if response.status_code != 200:
            write_log(f"error: get state {response.status_code} - {response.text}")
            return "error", ""
        state = response.json().get('state')
        media_content_id = response.json().get('attributes', {}).get('media_content_id', '')
        return state, media_content_id
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
    
def get_service_play(media_id, media_content_id, title):
    service_data = {
                'entity_id': media_id,
                'media_content_id': media_content_id,
                'media_content_type': 'music',
                "extra": {
                    "title": title
                    }
            }
    return service_data

def get_playlist_play(media_id, name, song_id, version):
    playlist = {}
    # get song info
    playlist[song_id] = return_song_info_from_id(media_id,song_id,version, name)  
    return playlist

def get_playlist_by_name(media_id, name, number, version):
    playlist = {}
    # get song info
    list_song_id = return_list_song_id_from_name(name, number)
    for song_id in list_song_id:
        playlist[song_id] = return_song_info_from_id(media_id, song_id,version, name)  
    return playlist

def get_playlist_from_id_url(list_id, media_id,  version):
    playlist = {}
    list_song_id = get_id_in_playlist(list_id)
    for song_id in list_song_id:
        playlist[song_id] = return_song_info_from_id(media_id, song_id, version)
    return playlist

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
    if response.status_code != 200:
        logger.error(f"Error fetching playlist items for ID {play_list}: {response.status_code} - {response.text}")
        return []
    list = json.loads(response.text)["items"]
    list_playlist=[]
    for lis in list:
        list_playlist.append(lis["snippet"]["resourceId"]["videoId"])
    return list_playlist

import os
import time

ENABLE_LOG = True  # Set this to False to disable logging

def write_log(msg):
    if not ENABLE_LOG:
        return
    
    log_file = "log.log"
    max_lines = 200
    remove_lines = 100

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_entry = f"{current_time}: {msg}\n"
    
    # Write the new log entry
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(log_entry)

    # Check and truncate the file if it exceeds the max lines
    try:
        with open(log_file, "r+", encoding="utf-8") as file:
            lines = file.readlines()
            if len(lines) > max_lines:
                # Remove the first `remove_lines` lines
                lines = lines[remove_lines:]
                # Rewrite the file with the remaining lines
                file.seek(0)  # Move to the start of the file
                file.truncate()  # Clear the file
                file.writelines(lines)  # Write the remaining lines back
    except Exception as e:
        print(f"Error while truncating log file: {e}")


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
    if response.status_code != 200:
        logger.error(f"Error fetching secondary results for ID {id}: {response.status_code} - {response.text}")
        return []

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

def read_data_from_json(file):
    try:
        with open(file, encoding="utf8") as f:
            data = json.load(f)
            if not data:
                return {}
            return data
    except json.JSONDecodeError:
        return {}

def write_data_to_json(file, data):
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(data, f,ensure_ascii=False, indent=4)

def get_best_stream_song(id):
    url_ytm = YTM_DOMAIN + "/watch?v=" + id
    video_url = ""
    length = 0
    song_name = ""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            start_time = time.time()
            info = ydl.extract_info(url_ytm, download=False)
            format_selector = ydl.build_format_selector("m4a/bestaudio")
            stream_format = next(format_selector({"formats": info["formats"]}), None)
            video_url = stream_format.get("url") if stream_format else None
            length = info.get("duration", None)
            song_name = info.get("title", None)
            print(f"Info extracted in {time.time() - start_time:.2f}s")
        except yt_dlp.utils.DownloadError as err:
            print(f"Error extracting info: {err}")
            return ""


    return video_url, length, song_name