
from flask import Response, request, stream_with_context
from model.stream import audio, stream_flac
from utils.utils_functions import read_data_from_json
from const import PLAYLIST_INFO_PATH
def music():
    timestamp = int(request.args.get("ts"))
    song_id = request.args.get("song_id")
    media_id = request.args.get("media_id")
    stream_url = get_info_from_unique_id(media_id, song_id)
    if not stream_url:
        return "Stream_url not found", 404
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

def get_info_from_unique_id(media_id, song_id):
    path = PLAYLIST_INFO_PATH + media_id + ".json"
    playlist= read_data_from_json(path)
    stream_url = ""
    for song_id_key, value in playlist.items():
        if song_id_key == song_id:
            stream_url = value.get("stream_url")
            break
    return stream_url
