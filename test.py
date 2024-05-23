# encoding: utf-8
import json
import random
from time import sleep
from urllib.parse import parse_qs, urlparse

import requests
import voluptuous as vol
from email.policy import default
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.helpers import config_validation as cv, service
from pytube import YouTube

from .youtube_assistant import *
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'youtube_assistant'

SERVICE_PLAY_SONG = 'play_song'
SERVICE_PLAY_LIST = 'play_list'
SERVICE_PLAY_NEXT = 'play_next'
SERVICE_PLAY_PREVIOUS = 'play_previous'

ATTR_NAME = 'name'
ATTR_SONG_ID = 'song_id'
ATTR_URL = 'url'
ATTR_NUMBER = 'number'
ATTR_LIST_ID = 'list_id'
ATTR_REPEAT = 'repeat'

SERVICE_SONG = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_SONG_ID, default=""): cv.string,
    vol.Optional(ATTR_URL, default=""): cv.string,
    vol.Optional(ATTR_NAME, default=""): cv.string,
    vol.Optional(ATTR_REPEAT, default=False): cv.boolean,
    vol.Optional(ATTR_NUMBER, default=0): cv.positive_int
})

SERVICE_LIST = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_LIST_ID, default=""): cv.string,
    vol.Optional(ATTR_URL, default=""): cv.string
})

SERVICE_NEXT = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_LIST_ID, default=""): cv.string,
    vol.Optional(ATTR_URL, default=""): cv.string,
    vol.Optional(ATTR_SONG_ID, default=""): cv.string,
    vol.Optional(ATTR_NAME, default=""): cv.string,
    vol.Optional(ATTR_REPEAT, default=False): cv.boolean,
    vol.Optional(ATTR_NUMBER, default=0): cv.positive_int
})

SERVICE_PREVIOUS = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_LIST_ID, default=""): cv.string,
    vol.Optional(ATTR_URL, default=""): cv.string,
    vol.Optional(ATTR_SONG_ID, default=""): cv.string,
    vol.Optional(ATTR_NAME, default=""): cv.string,
    vol.Optional(ATTR_REPEAT, default=False): cv.boolean,
    vol.Optional(ATTR_NUMBER, default=0): cv.positive_int
})
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

class PlayerMedia:
    def __init__(self, hass):
        self.hass = hass
        self.old_id_playlist = ''
        self.old_playlist = []
        self.id_song = ''
        self.stop = False

    def play_playlist(self, entity_id, list_playlist):
        for song_id in list_playlist:
            if self.stop:
                break
            _LOGGER.info("Playing song with ID: %s", song_id)
            self.id_song = song_id
            yt = YouTube(return_url_from_id(song_id))
            service_data = {
                'entity_id': entity_id,
                'media_content_id': return_url_from_id(song_id),
                'media_content_type': 'music',
                "extra": {
                    "thumb": yt.thumbnail_url,
                    "title": yt.title,
                    "enqueue":"true"
                }
            }
            self.hass.services.call('media_player', 'play_media', service_data)
            sleep(3)
            while True:
                state = self.hass.states.get(entity_id)
                if state.state == 'idle':
                    break
                sleep(1)

    def play_next(self, entity_id, list_playlist):
        current_index = list_playlist.index(self.id_song)
        if current_index < len(list_playlist) - 1:
            current_index += 1
        self.stop = True
        sleep(1)
        self.stop = False
        self.play_playlist(entity_id, list_playlist[current_index:])

    def play_previous(self, entity_id, list_playlist):
        current_index = list_playlist.index(self.id_song)
        if current_index > 0:
            current_index -= 1
        self.stop = True
        sleep(1)
        self.stop = False
        self.play_playlist(entity_id, list_playlist[current_index:])

    def tts_handler(self, service):
        entity_id = service.data[ATTR_ENTITY_ID]
        for entity in entity_id:
            if service.service == SERVICE_PLAY_LIST:
                list_id = service.data.get(ATTR_LIST_ID)
                url = service.data.get(ATTR_URL)
                list_playlist = get_playlist_from_id_url(list_id, url)
                self.old_id_playlist = list_id
                self.old_playlist = list_playlist
                self.play_playlist(entity, list_playlist)
            elif service.service == SERVICE_PLAY_SONG:
                song_id = service.data.get(ATTR_SONG_ID)
                url = service.data.get(ATTR_URL)
                number = service.data.get(ATTR_NUMBER)
                name = service.data.get(ATTR_NAME)
                repeat = service.data.get(ATTR_REPEAT)
                song_url, id = get_playlist_from_songid_name(song_id, url, name)
                self.old_id_playlist = id
                if repeat:
                    if number != 0:
                        list_playlist = [song_url] * number
                        self.old_playlist = list_playlist
                        self.play_playlist(entity, list_playlist)
                else:
                    if number != 0:
                        list_id_the_same = self.return_the_same_id(id, number)
                        self.old_playlist = list_id_the_same
                        self.play_playlist(entity, list_id_the_same)
            elif service.service == SERVICE_PLAY_NEXT:
                self.handle_next_previous(service, entity, True)
            elif service.service == SERVICE_PLAY_PREVIOUS:
                self.handle_next_previous(service, entity, False)

    def handle_next_previous(self, service, entity, is_next):
        list_id = service.data.get(ATTR_LIST_ID)
        song_id = service.data.get(ATTR_SONG_ID)
        url = service.data.get(ATTR_URL)
        number = service.data.get(ATTR_NUMBER)
        name = service.data.get(ATTR_NAME)
        repeat = service.data.get(ATTR_REPEAT)
        id = ''
        if name:
            song_url, id = get_playlist_from_songid_name(song_id, url, name)
        if list_id == self.old_id_playlist or id == self.old_id_playlist:
            list_playlist = self.old_playlist
            if is_next:
                self.play_next(entity, list_playlist)
            else:
                self.play_previous(entity, list_playlist)

    def register_services(self):
        self.hass.services.register(DOMAIN, SERVICE_PLAY_SONG, self.tts_handler, schema=SERVICE_SONG)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_LIST, self.tts_handler, schema=SERVICE_LIST)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_NEXT, self.tts_handler, schema=SERVICE_NEXT)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_PREVIOUS, self.tts_handler, schema=SERVICE_PREVIOUS)    

def setup(hass, config):
    youtube_assistant = PlayerMedia(hass)
    youtube_assistant.register_services()
    return True