def calculate_content_length(length_ms, bitrate_kbps):
    """
    Tính Content-Length (bytes) từ độ dài video (ms) và bitrate (kbps).
    """
    length_seconds = length_ms / 1000  # Chuyển đổi ms sang giây
    bitrate_bps = bitrate_kbps * 1000  # Chuyển kbps sang bps
    content_length = (bitrate_bps * length_seconds) / 8  # Tính số byte
    return int(content_length)  # Trả về giá trị nguyên

# Ví dụ:
length_ms = 93621  # Thời lượng video
bitrate_kbps = 192  # Bitrate cố định (192 kbps)
content_length = calculate_content_length(length_ms, bitrate_kbps)

print(f"Content-Length: {content_length} bytes")
print(f"Content-Length: {content_length / 1024} KB")