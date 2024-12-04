from flask import Flask, Response,request
from utils import *
from controllers import media
from controllers import stream
app = Flask(__name__)

#play media
@app.route('/media/play', methods=['POST'])
def play():
    """
    control media device to play list
    """
    return media.play()

#play playlist
@app.route('/media/play_playlist', methods=['POST'])
def play_playlist():
    """
    control media device to play list
    """
    return media.play_playlist()

#play next song
@app.route('/media/next', methods=['POST'])
def next():
    """
    control media device to play next song
    """
    return media.next()

#play previous song
@app.route('/media/previous', methods=['POST'])
def previous():
    """
    control media device to play previous song
    """
    return media.previous()

@app.route('/stream/<media_id>/<id>.flac')
def music(media_id, id):
    return stream.music(media_id, id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2024)
