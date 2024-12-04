# encoding: utf-8
import json
import requests
import random
from urllib.parse import parse_qs, urlparse
# Declare variables
DOMAIN = 'youtube_tts'
SERVICE_YOUTUBE_TTS = 'say'
# config
# CONF_API_KEY = 'api_key'
# data service
CONF_PLAYER_ID = 'entity_id'
CONF_MESSAGE = 'message'
CONF_URL = 'url'
def setup(hass, config):
    def return_url_from_name(name):
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
                return get_id_in_playlist(list[0])
            return parse_qs(urlparse(url).query).get("v")[0]
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
        return list[random.randint(0, len(list)-1)]["snippet"]["resourceId"]["videoId"]
    def tts_handler(data_call):
        # Get config
        # api_key = str(config[DOMAIN][CONF_API_KEY])      
        # Get data service
        # conf = config.get(DOMAIN)
        # media_id = conf.get(CONF_PLAYER_ID)
        # message = str(conf.get(CONF_MESSAGE)[0:2000])
        # url = str(conf.get(CONF_URL)[0:2000])
        media_id = data_call.data.get(CONF_PLAYER_ID)
        message = str(data_call.data.get(CONF_MESSAGE)[0:2000])
        url = str(data_call.data.get(CONF_URL)[0:2000])
        service_data = {}
        try:
            if (message != ""):
                song_url = return_url_from_name(message)
                # service data for 'CALL SERVICE' in Home Assistant
                service_data = {'entity_id': media_id, 'media_content_id': song_url, 'media_content_type': 'music'}
            else:
                # if (play_list != ""):
                #     song_url = return_url_from_id(get_id_in_playlist(play_list))
                #     service_data = {'entity_id': media_id, 'media_content_id': song_url, 'media_content_type': 'music'}
                # else: 
                song_url = return_url_from_url(url)
                service_data = {'entity_id': media_id, 'media_content_id': song_url, 'media_content_type': 'music'}
            # Call service from Home Assistant
        except:
            pass
        hass.services.call('media_extractor', 'play_media', service_data)
    hass.services.register(DOMAIN, SERVICE_YOUTUBE_TTS, tts_handler)
    return True
