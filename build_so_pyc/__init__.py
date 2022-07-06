from .youtube_assistant import *
import random
from urllib.parse import parse_qs, urlparse

DOMAIN = 'youtube_assistant'
SERVICE_YOUTUBE_ASSISTANT = 'play_song'
# config
# CONF_API_KEY = 'api_key'
# data service
CONF_PLAYER_ID = 'entity_id'
DEFAULT_PLAYER_ID = ''
CONF_NAME = 'name'
DEFAULT_NAME = ''
CONF_SONG_ID = 'song_id'
DEAFULT_SONG_ID = ''
DEFAULT_NAME = ''
CONF_URL = 'url'
DEFAULT_URL = ''
CONF_NUMBER = 'number'
DEFAULT_NUMBER = 5

def setup(hass, config):
    def clear_queue(entity_id):
        service_data = {'command': 'clear', 'entity_id': entity_id}
        hass.services.call('mass', 'queue_command', service_data)
    def tts_handler(data_call):
        entity_id = data_call.data.get(CONF_PLAYER_ID, DEFAULT_PLAYER_ID)
        name = str(data_call.data.get(CONF_NAME, DEFAULT_NAME)[0:2000])
        url = str(data_call.data.get(CONF_URL, DEFAULT_URL)[0:2000])
        song_id = str(data_call.data.get(CONF_SONG_ID, DEAFULT_SONG_ID))
        number = int(data_call.data.get(CONF_NUMBER, DEFAULT_NUMBER))
        service_data = {}
        clear_queue(entity_id)
        try:
            if (song_id != ""):
                song_url = return_url_from_id(song_id)
                list_id_the_same = return_the_same_id(song_id, number)
                # service data for 'CALL SERVICE' in Home Assistant
                service_data = {'entity_id': entity_id, 'uri': song_url, 'command': 'play_media'}
                hass.services.call('mass', 'queue_command', service_data)
                for ids in list_id_the_same:
                    service_data = {'entity_id': entity_id, 'uri': return_url_from_id(ids), 'command': 'play_media', 'mode': 'play_media_play_add'}
                    hass.services.call('mass', 'queue_command', service_data)
            elif (name != ""):
                id = return_id_from_name(name)
                song_url = return_url_from_id(id)
                list_id_the_same = return_the_same_id(id, number)
                # service data for 'CALL SERVICE' in Home Assistant
                service_data = {'entity_id': entity_id, 'uri': song_url, 'command': 'play_media'}
                hass.services.call('mass', 'queue_command', service_data)
                for ids in list_id_the_same:
                    service_data = {'entity_id': entity_id, 'uri': return_url_from_id(ids), 'command': 'play_media', 'mode': 'play_media_play_add'}
                    hass.services.call('mass', 'queue_command', service_data)
            else:
                if (getVideoId(url) != ""):
                    id = getVideoId(url)[0]
                    song_url = return_url_from_id(id)
                    list_id_the_same = return_the_same_id(id, number)
                    # service data for 'CALL SERVICE' in Home Assistant
                    service_data = {'entity_id': entity_id, 'uri': song_url, 'command': 'play_media'}
                    hass.services.call('mass', 'queue_command', service_data)
                    for ids in list_id_the_same:
                        service_data = {'entity_id': entity_id, 'uri': return_url_from_id(ids), 'command': 'play_media', 'mode': 'play_media_play_add'}
                        hass.services.call('mass', 'queue_command', service_data)
                else:
                    list = parse_qs(urlparse(url).query).get("list")
                    list_playlist = get_id_in_playlist(list[0])
                    service_data = {'entity_id': entity_id, 'uri': return_url_from_id(list_playlist[0]), 'command': 'play_media'}
                    hass.services.call('mass', 'queue_command', service_data)
                    for ids in list_playlist[1:]:
                        service_data = {'entity_id': entity_id, 'uri': return_url_from_id(ids), 'command': 'play_media', 'mode': 'play_media_play_add'}
                        hass.services.call('mass', 'queue_command', service_data)
            # Call service from Home Assistant
        except:
            pass
    hass.services.register(DOMAIN, SERVICE_YOUTUBE_ASSISTANT, tts_handler)
    return True