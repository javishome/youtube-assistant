# Service youtube assistant cho phép phát bài hát youtube dựa trên từ khóa

### _Khai báo trong configuration.yaml như sau:_

```sh
youtube_assistant:
media_extractor:
```   
### _Khai báo gọi dịch vụ như sau:_

```sh
service: youtube_assistant.play_song
data:
  entity_id: media_player.audiocast_quang
  song_id: qCA245x_T0o
  name: chắc ai đó sẽ về
  url: https://www.youtube.com/watch?v=cfbNtHNCMBo
  number: 10
```      
##### _Ý nghĩa của các trường_
- ```entity_id```: entity_id của thiết bị phát
- ```song_id```: id của bài hát trên youtube
- ```name```: tên của bài hát 
- ```url```: url của bài hát hoặc của play list
- ```number```: số lượng bài hát liên quan muốn phát (không áp dụng cho phát playlist) mặc định là 5
##### _Lưu ý :_
- ```entity_id``` là trường bắt buộc phải có
- ```song_id```, ```name```, ```url``` cần có thêm một trong ba trường này, nếu có hai hoặc ba trường thứ tự ưu tiên ```song_id``` -> ```name``` -> ```url```
- ```number``` chứa số lượng bài hát liên quan, khi phát playlist tất cả bài hát trong playlist sẽ được đưa vào hàng đợi, number sẽ không có ý nghĩa.