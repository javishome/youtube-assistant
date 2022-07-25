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

# Declare variables
DOMAIN = 'youtube_assistant'

SERVICE_PLAY_SONG = 'play_song'
SERVICE_PLAY_LIST = 'play_list'
SERVICE_PLAY_NAME = 'play_name'
# config
# CONF_API_KEY = 'api_key'
# data service
ATTR_PLAYER_ID = 'entity_id'
ATTR_NAME = 'name'
ATTR_SONG_ID = 'song_id'
ATTR_URL = 'url'
ATTR_NUMBER = 'number'
ATTR_LIST_ID = 'list_id'

SERVICE_SONG = vol.Schema({
    vol.Required(ATTR_PLAYER_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_SONG_ID, default=""): cv.string,
    vol.Optional(ATTR_URL, default=""): cv.string,
    vol.Optional(ATTR_NUMBER, default=5): cv.positive_int
})
SERVICE_LIST = vol.Schema({
    vol.Required(ATTR_PLAYER_ID): cv.comp_entity_ids,
    vol.Optional(ATTR_LIST_ID, default=""): cv.string,
    vol.Optional(ATTR_URL, default=""): cv.string
    
})
SERVICE_NAME = vol.Schema({
    vol.Required(ATTR_PLAYER_ID): cv.comp_entity_ids,
    vol.Required(ATTR_NAME): cv.string,
    vol.Optional(ATTR_NUMBER, default=5): cv.positive_int,
    vol.Optional(ATTR_URL, default=""): cv.string
})
def setup(hass, config):
    def clear_queue(entity_id):
        service_data = {'command': 'clear', 'entity_id': entity_id}
        hass.services.call('mass', 'queue_command', service_data)
    def tts_handler(service):

        entity_id = service.data[ATTR_PLAYER_ID]
        service_data = {}
        clear_queue(entity_id)
        if service.service == SERVICE_PLAY_NAME:
            # name = str(data_call.data.get(CONF_NAME, DEFAULT_NAME)[0:2000])
            name = service.data[ATTR_NAME]
            number = service.data.get(ATTR_NUMBER)
            id = return_id_from_name(name)
            song_url = return_url_from_id(id)
            list_id_the_same = return_the_same_id(id, number)
            # service data for 'CALL SERVICE' in Home Assistant
            service_data = {'entity_id': entity_id, 'uri': song_url, 'command': 'play_media'}
            hass.services.call('mass', 'queue_command', service_data)
            for ids in list_id_the_same:
                service_data = {'entity_id': entity_id, 'uri': return_url_from_id(ids), 'command': 'play_media', 'mode': 'play_media_play_add'}
                hass.services.call('mass', 'queue_command', service_data)
        elif service.service == SERVICE_PLAY_LIST:
            list_id = service.data.get(ATTR_LIST_ID)
            url = service.data.get(ATTR_URL)
            id = ""
            if (list_id != ""):
                id = list_id
            else:
                id = getListId(url)[0]
            list_playlist = get_id_in_playlist(id)
            service_data = {'entity_id': entity_id, 'uri': return_url_from_id(list_playlist[0]), 'command': 'play_media'}
            hass.services.call('mass', 'queue_command', service_data)
            for ids in list_playlist[1:]:
                service_data = {'entity_id': entity_id, 'uri': return_url_from_id(ids), 'command': 'play_media', 'mode': 'play_media_play_add'}
                hass.services.call('mass', 'queue_command', service_data)
        elif service.service == SERVICE_PLAY_SONG:
            song_id = service.data.get(ATTR_SONG_ID)
            url = service.data.get(ATTR_URL)
            id = ""
            number = service.data.get(ATTR_NUMBER)
            if (song_id != ""):
                id = song_id
            else:
                id = getVideoId(url)[0]
            song_url = return_url_from_id(id)
            list_id_the_same = return_the_same_id(id, number)
            # service data for 'CALL SERVICE' in Home Assistant
            service_data = {'entity_id': entity_id, 'uri': song_url, 'command': 'play_media'}
            hass.services.call('mass', 'queue_command', service_data)
            for ids in list_id_the_same:
                service_data = {'entity_id': entity_id, 'uri': return_url_from_id(ids), 'command': 'play_media', 'mode': 'play_media_play_add'}
                hass.services.call('mass', 'queue_command', service_data)
    hass.services.register(DOMAIN, SERVICE_PLAY_SONG, tts_handler, schema=SERVICE_SONG)
    hass.services.register(DOMAIN, SERVICE_PLAY_LIST, tts_handler, schema=SERVICE_LIST)
    hass.services.register(DOMAIN, SERVICE_PLAY_NAME, tts_handler, schema=SERVICE_NAME)
    return True