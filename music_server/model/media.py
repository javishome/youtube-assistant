
from utils.utils_functions import *
import multiprocessing
from const import PLAYLIST_INFO_PATH

class MediaControl:
    def __init__(self):
        self.processes = {}

mediaControl = MediaControl()

class Media:
    def __init__(self, media_id):
        self.media_id = media_id
        self.process_play_media = None
        self.manager = multiprocessing.Manager()

    def create_media_process(self):
        # Kill process if it is running
        if self.process_play_media and self.process_play_media.is_alive():
            self.process_play_media.terminate()
            write_log("finish process: " + self.media_id)
        
        # Clear the stop flag and start a new process
        playlist = self.playlist
        media_id = self.media_id
        self.process_play_media = multiprocessing.Process(target=play_media_in_process, args=(self.current_song_index,playlist, media_id))
        self.process_play_media.start()
        write_log("start process: " + self.media_id)
                    
    def play_media(self, playlist):
        self.playlist = playlist
        self.current_song_index = self.manager.Value('i', 0)
        self.create_media_process()

    def next(self):
        if self.current_song_index.value < len(self.playlist) - 1:
            self.current_song_index.value += 1
            self.create_media_process()

    def previous(self):
        if self.current_song_index.value > 0:
            self.current_song_index.value -= 1
            self.create_media_process()

def play_media_in_process(current_song_index, playlist, media_id):
    write_log(str(playlist))
    is_error = False
    # extract stream url of first song
    save_media_to_json(media_id, current_song_index.value)
    for idx, song_id in enumerate(playlist.keys()):
        if idx < current_song_index.value:
            continue
        current_song_index.value = idx
        length, name = get_song_info_from_file(media_id, current_song_index.value)
        timestamp = str(int(time.time()))
        media_content_id = playlist[song_id].get('url') + "&ts=" + timestamp
        
        write_log(f"change song: to {current_song_index.value}")
        # call service
        if length == 0:
            write_log("error: duration is 0 with " + song_id )
            continue
        call_play(media_id, media_content_id, name)
        # extract next song stream url
        if idx < len(playlist) - 1:
            save_media_to_json(media_id, current_song_index.value + 1)
        # wait for media to play
        count = 0
        while True:
            time.sleep(1)
            state = get_state(media_id)
            if state == "playing":
                break
            count +=1
            if count > 30:
                write_log("error: media not work with" + song_id)
                is_error = True
                break
        if is_error:
            break
        # wait to media end playing
        write_log("duration: " + str(length))
        start_time = time.time()
        pause_seconds = 0
        while True:
            duration_real = time.time() - start_time
            time.sleep(5)
            state = get_state(media_id)
            if state == "idle":
                write_log("finish: " + song_id)
                break
            elif state == "paused":
                write_log("paused: " + song_id)
                pause_seconds += 5
            elif state == "playing":
                write_log("playing: " + song_id)
            elif state == "Off":
                write_log("off: " + song_id)
                break

            if duration_real - pause_seconds > length:
                call_stop(media_id)
                write_log("finish: " + song_id)
                break
        state = get_state(media_id)
        if state.lower() == "off":
            write_log("error: media off" + song_id)
            break

def save_media_to_json(media_id, song_index):
    path = PLAYLIST_INFO_PATH + media_id + ".json"
    playlist = read_data_from_json(path)
    for idx, song_id in enumerate(playlist.keys()):
        if idx == song_index:
            song_id = playlist[song_id].get('id')
            if playlist[song_id].get("version") == 1:
                continue
            if not playlist[song_id].get("stream_url"):
                url, length, name = get_best_stream_song(song_id)
                playlist[song_id]["stream_url"] = url
                playlist[song_id]["length"] = length
                if playlist[song_id].get("name") == "" or not playlist[song_id].get("name"):
                    playlist[song_id]["name"] = name
            break
    write_data_to_json(path, playlist)

def get_song_info_from_file(media_id, song_index):
    path = PLAYLIST_INFO_PATH + media_id + ".json"
    playlist = read_data_from_json(path)
    length = 0
    name = ""
    for idx, song_id in enumerate(playlist.keys()):
        if idx == song_index:
            length = playlist[song_id].get('length')
            name = playlist[song_id].get('name')
            break
    return length, name