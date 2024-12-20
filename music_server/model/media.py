
from utils import *
import multiprocessing


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
        if self.process_play_media:
            self.process_play_media.terminate()
            write_log("finish process: " + self.media_id)
        
        # Clear the stop flag and start a new process
        self.process_play_media = multiprocessing.Process(target=self.play_media_in_process, args=(self.current_song_index,))
        self.process_play_media.start()
        write_log("start process: " + self.media_id)

    
    def play_media_in_process(self, current_song_index):
        write_log(str(self.playlist))
        is_error = False
        for idx, media_content_id in enumerate(self.playlist):
            if idx < current_song_index.value:
                continue
            current_song_index.value = idx
            write_log(f"change song: to {current_song_index.value}  in media: {self.media_id}")
            # call service
            duration = get_duration(media_content_id)
            if duration == 0:
                write_log("error: duration is 0" + media_content_id + " in media: " + self.media_id)
                continue
            call_play(self.media_id, media_content_id)
            # wait for media to play
            count = 0
            while True:
                time.sleep(1)
                state = get_state(self.media_id)
                if state == "playing":
                    break
                count +=1
                if count > 60:
                    write_log("error: media not work" + media_content_id + " in media: " + self.media_id)
                    is_error = True
                    break
            if is_error:
                break
            # wait to media end playing
            write_log("duration: " + str(duration) + " in media: " + self.media_id)
            start_time = time.time()
            pause_seconds = 0
            while True:
                duration_real = time.time() - start_time
                time.sleep(5)
                state = get_state(self.media_id)
                if state == "idle":
                    write_log("finish: " + media_content_id + " in media: " + self.media_id)
                    break
                elif state == "paused":
                    write_log("paused: " + media_content_id + " in media: " + self.media_id)
                    pause_seconds += 5
                elif state == "playing":
                    write_log("playing: " + media_content_id + " in media: " + self.media_id)
                elif state == "Off":
                    write_log("off: " + media_content_id + " in media: " + self.media_id)
                    break

                if duration_real - pause_seconds > duration:
                    write_log("finish: " + media_content_id + " in media: " + self.media_id)
                    break
            state = get_state(self.media_id)
            if state.lower() == "off":
                write_log("error: media off" + media_content_id + " in media: " + self.media_id)
                break
                    
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