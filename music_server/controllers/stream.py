
from flask import Response, request, stream_with_context
from model.stream import audio, stream_flac
from utils import return_url_from_id_javis
def music(media_id, id):
    timestamp = int(request.args.get('ts'))
    process = audio.processes.get(media_id)
    if process:
        if timestamp < process["timestamp"]:
            return "Timestamp is too old", 400
    url_youtube = return_url_from_id_javis(id)
    response = Response(stream_with_context(stream_flac(url_youtube, media_id, timestamp)), content_type='audio/flac', headers={"Transfer-Encoding": "chunked"})
    # Truyền stream flac cho client
    return response