# encoding: utf-8
import requests
import voluptuous as vol
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.helpers import config_validation as cv, service

import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'youtube_assistant'

SERVICE_PLAY_SONG = 'play_song'
SERVICE_PLAY_MEDIA = 'play_media'
SERVICE_PLAY_LIST = 'play_list'
SERVICE_PLAY_LIST_STREAM = 'play_list_stream'
SERVICE_PLAY_SONG_TITLE = 'play_song_title'
SERVICE_PLAY_SONG_TITLE_STREAM = 'play_song_title_stream'
SERVICE_PLAY_NEXT = 'play_next'
SERVICE_PLAY_PREVIOUS = 'play_previous'

ATTR_NAME = 'name'
ATTR_SONG_ID = 'song_id'
ATTR_URL = 'url'
ATTR_LIST_ID = 'list_id'
ATTR_TITLE = 'song_title'
ATTR_NUMBER = 'number'

SERVICE_SONG = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_SONG_ID, default=""): cv.string,
    # vol.Optional(ATTR_URL, default=""): cv.string,
    vol.Optional(ATTR_NAME, default=""): cv.string,
})

SERVICE_SONG_OLD = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_SONG_ID, default=""): cv.string,
    # vol.Optional(ATTR_URL, default=""): cv.string,
    vol.Optional(ATTR_NAME, default=""): cv.string,
    vol.Optional(ATTR_NUMBER, default=1): cv.Number,
})

SERVICE_LIST = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_LIST_ID, default=""): cv.string,
    # vol.Optional(ATTR_URL, default=""): cv.string,
})

SERVICE_SONG_TITLE = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_TITLE, default=""): cv.string,
    vol.Optional(ATTR_NUMBER, default=1): cv.Number,
})

SERVICE_NEXT = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
})

SERVICE_PREVIOUS = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
})

class PlayerMedia:
    def __init__(self, hass):
        self.hass = hass
        self.url = "http://localhost:2024"

    def tts_handler(self, service):
        entity_id = service.data[ATTR_ENTITY_ID]
        for entity in entity_id:
            if service.service == SERVICE_PLAY_LIST:
                list_id = service.data.get(ATTR_LIST_ID)
                # url = service.data.get(ATTR_URL)
                api_playlist = "/media/play_playlist"
                data = {
                    "media_id": entity,
                    "list_id": list_id,
                    # "url": url,
                    "version": "1"
                }
                requests.post(self.url + api_playlist, json=data)

            elif service.service == SERVICE_PLAY_LIST_STREAM:
                list_id = service.data.get(ATTR_LIST_ID)
                # url = service.data.get(ATTR_URL)
                api_playlist = "/media/play_playlist"
                data = {
                    "media_id": entity,
                    "list_id": list_id,
                    # "url": url,
                    "version": "2"
                }
                requests.post(self.url + api_playlist, json=data)

            elif service.service == SERVICE_PLAY_SONG:
                song_id = service.data.get(ATTR_SONG_ID)
                # url = service.data.get(ATTR_URL)
                name = service.data.get(ATTR_NAME)
                api_play = "/media/play"
                data = {
                    "media_id": entity,
                    "song_id": song_id,
                    # "url": url,
                    "name": name,
                    "version": "1"
                }
                requests.post(self.url + api_play, json=data)
            elif service.service == SERVICE_PLAY_MEDIA:
                song_id = service.data.get(ATTR_SONG_ID)
                # url = service.data.get(ATTR_URL)
                name = service.data.get(ATTR_NAME)
                api_play = "/media/play"
                data = {
                    "media_id": entity,
                    "song_id": song_id,
                    # "url": url,
                    "name": name,
                    "version": "2"
                }
                requests.post(self.url + api_play, json=data)

            elif service.service == SERVICE_PLAY_SONG_TITLE:
                song_id = service.data.get(ATTR_SONG_ID)
                song_title = service.data.get(ATTR_TITLE)
                number = service.data.get(ATTR_NUMBER)
                api_play = "/media/play_by_name"
                data = {
                    "media_id": entity,
                    "name": song_title,
                    "number": number,
                    "version": "1"
                }
                requests.post(self.url + api_play, json=data)

            elif service.service == SERVICE_PLAY_SONG_TITLE_STREAM:
                song_id = service.data.get(ATTR_SONG_ID)
                song_title = service.data.get(ATTR_TITLE)
                number = service.data.get(ATTR_NUMBER)
                api_play = "/media/play_by_name"
                data = {
                    "media_id": entity,
                    "name": song_title,
                    "number": number,
                    "version": "2"
                }
                requests.post(self.url + api_play, json=data)
  
            elif service.service == SERVICE_PLAY_NEXT:
                _LOGGER.info("Next")
                data = {
                    "media_id": entity
                }
                requests.post(self.url + "/media/next", json=data)

            elif service.service == SERVICE_PLAY_PREVIOUS:
                _LOGGER.info("Previous")
                data = {
                    "media_id": entity
                }
                requests.post(self.url + "/media/previous", json=data)

    def register_services(self):
        self.hass.services.register(DOMAIN, SERVICE_PLAY_SONG, self.tts_handler, schema=SERVICE_SONG_OLD)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_MEDIA, self.tts_handler, schema=SERVICE_SONG)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_LIST, self.tts_handler, schema=SERVICE_LIST)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_LIST_STREAM, self.tts_handler, schema=SERVICE_LIST)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_NEXT, self.tts_handler, schema=SERVICE_NEXT)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_PREVIOUS, self.tts_handler, schema=SERVICE_PREVIOUS)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_SONG_TITLE, self.tts_handler, schema=SERVICE_SONG_TITLE)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_SONG_TITLE_STREAM, self.tts_handler, schema=SERVICE_SONG_TITLE) 

def setup(hass, config):
    youtube_assistant = PlayerMedia(hass)
    youtube_assistant.register_services()
    return True