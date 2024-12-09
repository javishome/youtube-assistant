# encoding: utf-8
import requests
import voluptuous as vol
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.helpers import config_validation as cv, service

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
ATTR_VERSION = 'version'

SERVICE_SONG = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_SONG_ID, default=""): cv.string,
    vol.Optional(ATTR_URL, default=""): cv.string,
    vol.Optional(ATTR_NAME, default=""): cv.string,
    vol.Optional(ATTR_REPEAT, default=False): cv.boolean,
    vol.Optional(ATTR_NUMBER, default=0): cv.positive_int,
    vol.Optional(ATTR_VERSION, default=""): cv.string
})

SERVICE_LIST = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_LIST_ID, default=""): cv.string,
    vol.Optional(ATTR_URL, default=""): cv.string,
    vol.Optional(ATTR_VERSION, default=""): cv.string
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
                url = service.data.get(ATTR_URL)
                version = service.data.get(ATTR_VERSION)
                api_playlist = "/media/play_playlist"
                data = {
                    "media_id": entity,
                    "list_id": list_id,
                    "url": url,
                    "version": version
                }
                requests.post(self.url + api_playlist, json=data)

            elif service.service == SERVICE_PLAY_SONG:
                song_id = service.data.get(ATTR_SONG_ID)
                url = service.data.get(ATTR_URL)
                number = service.data.get(ATTR_NUMBER)
                name = service.data.get(ATTR_NAME)
                repeat = service.data.get(ATTR_REPEAT)
                version = service.data.get(ATTR_VERSION)
                api_play = "/media/play"
                data = {
                    "media_id": entity,
                    "song_id": song_id,
                    "url": url,
                    "number": number,
                    "name": name,
                    "repeat": repeat,
                    "version": version
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
        self.hass.services.register(DOMAIN, SERVICE_PLAY_SONG, self.tts_handler, schema=SERVICE_SONG)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_LIST, self.tts_handler, schema=SERVICE_LIST)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_NEXT, self.tts_handler, schema=SERVICE_NEXT)
        self.hass.services.register(DOMAIN, SERVICE_PLAY_PREVIOUS, self.tts_handler, schema=SERVICE_PREVIOUS)    

def setup(hass, config):
    youtube_assistant = PlayerMedia(hass)
    youtube_assistant.register_services()
    return True