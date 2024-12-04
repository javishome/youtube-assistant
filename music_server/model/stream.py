import subprocess
from const import FFMPEG_PATH

class AudioStreamer:
    def __init__(self):
        self.processes = {}
audio = AudioStreamer()

def stream_flac(url, media_id, timestamp):
    
    
    # Kết thúc và giải phóng tiến trình ffmpeg hiện tại nếu tồn tại
    if audio.processes.get(media_id):
        audio.processes[media_id]["process"].kill()  # Kết thúc tiến trình ffmpeg cũ
        audio.processes[media_id]["process"].wait()  # Đợi cho tiến trình kết thúc hoàn toàn

    # Lệnh ffmpeg để chuyển đổi mp3 sang flac và truyền stream qua stdout
    command = [
        FFMPEG_PATH,
        "-i", url,
        "-vn",
        "-acodec", "flac",
        "-f", "flac",
        "-buffer_size", "8K",   # Giới hạn bộ đệm
        "-max_delay", "1000000", # Giảm độ trễ
        "pipe:1"
    ]

    # Tạo tiến trình ffmpeg mới
    audio.processes[media_id] = {
        "process": subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE),
        "timestamp": timestamp
    }        
    try:
        # Đọc và truyền từng phần nhỏ của luồng stdout để giảm thiểu tải bộ nhớ
        while True:
            if not audio.processes.get(media_id):
                break
            chunk = audio.processes[media_id]["process"].stdout.read(1024)  # Đọc 1KB mỗi lần để tối ưu
            if not chunk:
                break
            yield chunk
    finally:
        # Đảm bảo tiến trình ffmpeg được giải phóng hoàn toàn
        if audio.processes.get(media_id):
            audio.processes[media_id]["process"].kill()
            audio.processes[media_id]["process"].wait()
            # del audio.processes[media_id]  # Giải phóng tham chiếu tới tiến trình cũ