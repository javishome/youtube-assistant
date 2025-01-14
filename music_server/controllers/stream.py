
from flask import Response, request, stream_with_context
from model.stream import audio, stream_flac
from utils import read_data_from_json

def music():
    timestamp = int(request.args.get("ts"))
    media_song_id = request.args.get("media_song_id")
    media_id, stream_url = get_info_from_unique_id(media_song_id)
    process = audio.processes.get(media_id)
    if process:
        if timestamp < process["timestamp"]:
            return "Timestamp is too old", 400
    headers = {
        "Accept-Ranges": "bytes",
        "Content-Type": "audio/mp3",
        "Connection": "keep-alive",
        "Timeout": "5",
    }

    response = Response(stream_with_context(stream_flac(stream_url, media_id, timestamp)), headers=headers)
    # Truyền stream flac cho client
    return response

def get_info_from_unique_id(media_song_id):
    playlists_dict = read_data_from_json("playlists.json")
    for media_id, media_value in playlists_dict.items():
        for key, value in media_value.items():
            if media_song_id == key:
                stream_url = value.get("stream_url")
                break
    return media_id, stream_url
