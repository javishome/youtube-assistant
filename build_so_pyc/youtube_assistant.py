# encoding: utf-8
import json
import requests
import random
from urllib.parse import parse_qs, urlparse
def return_id_from_name(name):
    url = "https://www.youtube.com/youtubei/v1/search?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    payload = json.dumps({   
        "context": {
            "client": {
                "hl": "vi",
                "gl": "VN",
                "deviceMake": "Apple",
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_5) AppleWebKit/544.35 (KHTML, like Gecko) Chrome/84.5.4003.207 Safari/539.31,gzip(gfe)",
                "clientName": 1,
                "clientVersion": "2.20220411.09.00",
                "osName": "Macintosh",
                "osVersion": "10_5_5",
                "platform": "DESKTOP",
                "configInfo": {
                    "appInstallData": "CL3c2pIGELfLrQUQmOqtBRDUg64FEPCCrgUQjdz9EhDYvq0FEJH4_BI%3D"
                },
                "screenDensityFloat": 2,
                "browserName": "Chrome",
                "browserVersion": "84.5.4003.207",
                "mainAppWebInfo": {
                    "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                    "graftUrl": "/results?search_query=s%C3%B3ng+gi%C3%B3"
                },
                "connectionType": "CONN_CELLULAR_4G"
            },
            "request": {
                "useSsl": True,
                "internalExperimentFlags": [],
                "consistencyTokenJars": []
            },
            "adSignalsInfo": {
                "consentBumpParams": {
                    "consentHostnameOverride": "https://www.youtube.com",
                    "urlOverride": ""
                }
            },
            "user": {
                "lockedSafetyMode": False
            },
            "clickTracking": {
                "clickTrackingParams": "CJwBELsvGAIiEwjHlr2k8pD3AhWDS_UFHbZaBYE="
            }
        },
        "query": name
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'GPS=1; VISITOR_INFO1_LIVE=vUmkdIJ9Ivg; YSC=1Uj5v_ZJfRA'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    result = json.loads(response.text)["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
        "sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["videoRenderer"]["videoId"]
    return result
def return_url_from_id(result):
    url = "https://youtubei.googleapis.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"

    payload = json.dumps({
        "context": {
            "client": {
                "hl": "vi-VN",
                "clientName": "ANDROID",
                "gl": "VN",
                "clientVersion": "16.29.38"
            },
            "user": {
                "lockedSafetyMode": False
            }
        },
        "videoId": result
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    result = json.loads(response.text)["streamingData"]["formats"][0]["url"]
    return result
def getVideoId(url):
    if (url.find('watch?v=') != -1):
        list = parse_qs(urlparse(url).query).get("list")
        if list != None:
            return ""
        return parse_qs(urlparse(url).query).get("v")
    elif (url.find('youtu.be/') != -1):
        urstart_id_idex = url.find('youtu.be/') + len("youtu.be/")
        id = url[urstart_id_idex:]
        return id
    return ""
def return_url_from_id(id):
    url = "https://youtubei.googleapis.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    payload = json.dumps({
        "context": {
            "client": {
                "hl": "vi-VN",
                "clientName": "ANDROID",
                "gl": "VN",
                "clientVersion": "16.29.38"
            },
            "user": {
                "lockedSafetyMode": False
            }
        },
        "videoId": id
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    result = json.loads(response.text)["streamingData"]["formats"][0]["url"]
    return result
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