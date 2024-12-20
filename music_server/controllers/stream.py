
from flask import Response, request, stream_with_context
from model.stream import audio, stream_flac
from utils import return_url_from_id_javis, return_url_from_id_javis_v2
def music(media_id, id):
    timestamp = int(request.args.get("ts"))
    process = audio.processes.get(media_id)
    if process:
        if timestamp < process["timestamp"]:
            return "Timestamp is too old", 400
    url_youtube = return_url_from_id_javis(id)
    url, length = return_url_from_id_javis_v2(id)
    headers = {
        "Accept-Ranges": "bytes",
        "Content-Type": "audio/flac",
        "Connection": "keep-alive",
        "Timeout": "5",
        "Content-Length": str(length*24),
    }

    response = Response(stream_with_context(stream_flac(url_youtube, media_id, timestamp)), headers=headers)
    # Truyền stream flac cho client
    return response