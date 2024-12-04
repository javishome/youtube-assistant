# encoding: utf-8
from email.policy import default
import json
from numpy import number
import requests
import random
from urllib.parse import parse_qs, urlparse
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.helpers import config_validation as cv, service
import voluptuous as vol
from .youtube_assistant import *
import logging
from pytube import YouTube
_LOGGER = logging.getLogger(__name__)
# Declare variables
DOMAIN = 'youtube_assistant'

SERVICE_PLAY_SONG = 'play_song'
SERVICE_PLAY_LIST = 'play_list'
SERVICE_PLAY_NEXT='play_next'
SERVICE_PLAY_PREVIOUS='play_previous'
# config
# CONF_API_KEY = 'api_key'
# data service
# ATTR_PLAYER_ID = 'entity_id'
ATTR_NAME = 'name'
ATTR_SONG_ID = 'song_id'
ATTR_URL = 'url'
ATTR_NUMBER = 'number'
ATTR_LIST_ID = 'list_id'
ATTR_REPEAT = 'repeat'
ID_SONG = ''
OLD_ID_PLAYLIST=''
OLD_PLAYLIST = []

SERVICE_SONG = vol.Schema({
        vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
        vol.Optional(ATTR_SONG_ID, default=""): cv.string,
        vol.Optional(ATTR_URL, default=""): cv.string,
        vol.Optional(ATTR_NAME, default=""): cv.string,
        vol.Optional(ATTR_REPEAT, default=False): cv.boolean,
        vol.Optional(ATTR_NUMBER, default=0): cv.positive_int
    }
)
SERVICE_LIST = vol.Schema({
        vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
        vol.Optional(ATTR_LIST_ID, default=""): cv.string,
        vol.Optional(ATTR_URL, default=""): cv.string   
    }
)
SERVICE_NEXT = vol.Schema({
        vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
        vol.Optional(ATTR_LIST_ID, default=""): cv.string,
        vol.Optional(ATTR_URL, default=""): cv.string,
        vol.Optional(ATTR_SONG_ID, default=""): cv.string,
        vol.Optional(ATTR_NAME, default=""): cv.string,
        vol.Optional(ATTR_REPEAT, default=False): cv.boolean,
        vol.Optional(ATTR_NUMBER, default=0): cv.positive_int
    }
)
SERVICE_PREVIOUS = vol.Schema({
        vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
        vol.Optional(ATTR_LIST_ID, default=""): cv.string,
        vol.Optional(ATTR_URL, default=""): cv.string,
        vol.Optional(ATTR_SONG_ID, default=""): cv.string,
        vol.Optional(ATTR_NAME, default=""): cv.string,
        vol.Optional(ATTR_REPEAT, default=False): cv.boolean,
        vol.Optional(ATTR_NUMBER, default=0): cv.positive_int
    }
)

from time import sleep
global stop
stop =False
def play_playlist(hass, entity_id, list_playlist,stop):
    for song_id in list_playlist:
        # Phát bài hát
        if stop == True:
            break
        else:
            _LOGGER.info("Đang phát bài song_id: %s", song_id)
            global ID_SONG
            ID_SONG = song_id
            yt = YouTube(return_url_from_id(song_id))
            service_data = {'entity_id': entity_id, 'media_content_id': return_url_from_id(song_id), 'media_content_type': 'music',"extra": {"thumb": yt.thumbnail_url,"title": yt.title,"enqueue":"true"}}
            hass.services.call('media_player', 'play_media', service_data)
            #Đợi một khoảng thời gian ngắn trước check state
            sleep(3)
            while True:
                # Lấy state của media player
                state = hass.states.get(entity_id)
                # _LOGGER.info("state: %s", state.state)
                # Nếu state là idle thì bài hát đã kết thúc ->break
                if state.state == 'idle':
                    break
                sleep(1)

def play_next(hass, entity_id,list_playlist):
    # Lấy index hiện tại
    current_index = list_playlist.index(ID_SONG)
    # Nếu index hiện tại nhỏ hơn độ dài playlist - 1 thì tăng index lên 1
    if current_index < len(list_playlist) - 1:
        current_index += 1
    # Phát bài hát tiếp theo
    stop = True
    sleep(1)
    stop = False
    play_playlist(hass, entity_id, list_playlist[current_index:],stop)

def play_previous(hass, entity_id, list_playlist):
    # Lấy index hiện tại
    current_index = list_playlist.index(ID_SONG)
    # Nếu index hiện tại lớn hơn 0 thì giảm index đi 1
    if current_index > 0:
        current_index -= 1
    # Phát bài hát trước đó
    stop= True
    sleep(1)
    stop = False
    _LOGGER.info("list song_id: %s",list_playlist[current_index:])
    play_playlist(hass, entity_id, list_playlist[current_index:],stop)

def get_playlist_from_id_url(list_id, url):
    id=''
    if (list_id != ""):
        id = list_id
    else:
        id = getListId(url)[0]
    list_playlist = get_id_in_playlist(id)
    return list_playlist

def get_playlist_from_songid_name(song_id,url,name):
    id = ""
    if (song_id != ""):
        id = song_id
    elif (url != ""):
        id = getVideoId(url)[0]
    else: 
        id = return_id_from_name(name)
    song_url = return_url_from_id(id)  
    return song_url,id 

def setup(hass, config):

    def tts_handler(service):

        entity_id = service.data[ATTR_ENTITY_ID]
        service_data = {}
        service_play = {'entity_id': entity_id, 'command': 'play'}
        global OLD_ID_PLAYLIST
        global OLD_PLAYLIST
        for entity in entity_id:
            if service.service == SERVICE_PLAY_LIST:
                list_id = service.data.get(ATTR_LIST_ID)
                _LOGGER.info("-"*20)
                url = service.data.get(ATTR_URL)
                list_playlist = get_playlist_from_id_url(list_id, url)
                _LOGGER.info("list song_id: %s", list_playlist)
                _LOGGER.info("-"*20)
                OLD_ID_PLAYLIST = list_id
                OLD_PLAYLIST = list_playlist
                play_playlist(hass, entity, list_playlist,stop)
            elif service.service == SERVICE_PLAY_SONG:
                song_id = service.data.get(ATTR_SONG_ID)
                url = service.data.get(ATTR_URL)
                number = service.data.get(ATTR_NUMBER)
                name = service.data.get(ATTR_NAME)
                repeat = service.data.get(ATTR_REPEAT)
                song_url,id = get_playlist_from_songid_name(song_id,url,name)
                OLD_ID_PLAYLIST = id
                if (repeat == True):
                    if number != 0:
                        list_playlist = [song_url]*number
                        OLD_PLAYLIST = list_playlist
                        play_playlist(hass, entity, list_playlist,stop)
                else:
                    if number != 0:
                        list_id_the_same = return_the_same_id(id, number)
                        OLD_PLAYLIST = list_id_the_same
                        play_playlist(hass, entity, list_id_the_same,stop)
            elif service.service == SERVICE_PLAY_NEXT:
                list_id = service.data.get(ATTR_LIST_ID)
                song_id = service.data.get(ATTR_SONG_ID)
                url = service.data.get(ATTR_URL)
                number = service.data.get(ATTR_NUMBER)
                name = service.data.get(ATTR_NAME)
                repeat = service.data.get(ATTR_REPEAT)
                id=''
                if name:
                    song_url,id = get_playlist_from_songid_name(song_id,url,name)
                if (list_id == OLD_ID_PLAYLIST or id == OLD_ID_PLAYLIST):
                    list_playlist = OLD_PLAYLIST
                    play_next(hass, entity, list_playlist)
            elif service.service == SERVICE_PLAY_PREVIOUS:
                list_id = service.data.get(ATTR_LIST_ID)
                song_id = service.data.get(ATTR_SONG_ID)
                url = service.data.get(ATTR_URL)
                number = service.data.get(ATTR_NUMBER)
                name = service.data.get(ATTR_NAME)
                repeat = service.data.get(ATTR_REPEAT)
                id=''
                if name:
                    song_url,id = get_playlist_from_songid_name(song_id,url,name)
                if (list_id == OLD_ID_PLAYLIST or id == OLD_ID_PLAYLIST):
                    list_playlist = OLD_PLAYLIST
                    play_previous(hass, entity, list_playlist)


    hass.services.register(DOMAIN, SERVICE_PLAY_SONG, tts_handler, schema=SERVICE_SONG)
    hass.services.register(DOMAIN, SERVICE_PLAY_LIST, tts_handler, schema=SERVICE_LIST)
    hass.services.register(DOMAIN, SERVICE_PLAY_NEXT, tts_handler, schema=SERVICE_NEXT)
    hass.services.register(DOMAIN, SERVICE_PLAY_PREVIOUS, tts_handler, schema=SERVICE_PREVIOUS)

    return True