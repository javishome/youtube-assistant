from flask import request
from utils.utils_functions import *
from model.media import Media, mediaControl
from const import PLAYLIST_INFO_PATH

def play():
    """
    control media device to play list
    """
    # step 2: get data from request
    data = request.get_json()
    if not data:
        return "Bad request", 400
    # step 3: check if data is valid
    if not data.get('media_id'):
        return "Bad request", 400
    media_id = data.get('media_id')
    song_id = data.get('song_id')
    name = data.get('name')
    version = int(data.get('version'))
    # step 4: process data
    if mediaControl.processes.get(media_id):
        media = mediaControl.processes[media_id]
    else:
        media = Media(media_id)
        mediaControl.processes[media_id] = media
    # extract playlist and save to json file
    path = PLAYLIST_INFO_PATH + media_id + ".json"
    playlist = get_playlist_play(media_id, name, song_id, version)
    write_data_to_json(path, playlist)
    # play media
    media.play_media(playlist)
    return "Success", 200

def play_playlist():
    """
    control media device to play list
    """
    # step 2: get data from request
    data = request.get_json()
    if not data:
        return "Bad request", 400
    # step 3: check if data is valid
    if not data.get('media_id'):
        return "Bad request", 400
    media_id = data.get('media_id')
    list_id = data.get('list_id')
    version = int(data.get('version'))
    # step 4: process data
    if mediaControl.processes.get(media_id):
        media = mediaControl.processes[media_id]
    else:
        media = Media(media_id)
    mediaControl.processes[media_id] = media
    # extract playlist and save to json file
    path = PLAYLIST_INFO_PATH + media_id + ".json"
    playlist = get_playlist_from_id_url(list_id, media_id,  version)
    write_data_to_json(path, playlist)
    # play media
    media.play_media(playlist)
    return "Success", 200

def play_by_name():
    """
    control media device to play list
    """
    # step 2: get data from request
    data = request.get_json()
    if not data:
        return "Bad request", 400
    # step 3: check if data is valid
    if not data.get('media_id'):
        return "Bad request", 400
    media_id = data.get('media_id')
    name = data.get('name')
    number = int(data.get('number'))
    version = int(data.get('version'))
    # step 4: process data
    if mediaControl.processes.get(media_id):
        media = mediaControl.processes[media_id]
    else:
        media = Media(media_id)
        mediaControl.processes[media_id] = media
    # extract playlist and save to json file
    path = PLAYLIST_INFO_PATH + media_id + ".json"
    playlist = get_playlist_by_name(media_id, name,number, version)
    write_data_to_json(path, playlist)
    # play media
    media.play_media(playlist)
    return "Success", 200


def next():
    """
    control media device to play next song
    """
    # step 2: get data from request
    data = request.get_json()
    if not data:
        return "Bad request", 400
    # step 3: check if data is valid
    if not data.get('media_id'):
        return "Bad request", 400
    media_id = data.get('media_id')
    # step 4: process data
    if mediaControl.processes.get(media_id):
        media = mediaControl.processes[media_id]
    else:
        return "Media not found", 404
    media.next()
    return "Success", 200

def previous():
    """
    control media device to play previous song
    """
    # step 2: get data from request
    data = request.get_json()
    if not data:
        return "Bad request", 400
    # step 3: check if data is valid
    if not data.get('media_id'):
        return "Bad request", 400
    media_id = data.get('media_id')
    # step 4: process data
    if mediaControl.processes.get(media_id):
        media = mediaControl.processes[media_id]
    else:
        return "Media not found", 404
    media.previous()
    return "Success", 200