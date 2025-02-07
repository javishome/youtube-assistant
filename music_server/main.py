from flask import Flask
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

#play by name
@app.route('/media/play_by_name', methods=['POST'])
def play_by_name():
    """
    control media device to play by name
    """
    return media.play_by_name()

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

@app.route('/stream')
def music():
    return stream.music()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2024)
