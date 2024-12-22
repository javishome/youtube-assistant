# Service youtube assistant cho phép phát bài hát youtube dựa trên từ khóa

### Khai báo trong configuration.yaml như sau:

```sh
youtube_assistant:
media_extractor:
```   
### Khai báo gọi dịch vụ như sau:
#### _Phát bài hát dựa theo ```song_id``` hoặc ```url``` hoặc ```name``` của bài hát ( Gọi trực tiếp từ server Javis):_
```sh
service: youtube_assistant.play_song
data:
  entity_id: media_player.audiocast_quang
  song_id: cfbNtHNCMBo
  url: https://www.youtube.com/watch?v=cfbNtHNCMBo
  name: chắc ai đó sẽ về
```      
##### _Ý nghĩa của các trường_
- ```entity_id```: entity_id của thiết bị phát
- ```song_id```: id của bài hát 
- ```url```: url của bài hát 
- ```name```: name của bài hát (ưu tiên ```song_id``` > ```url``` > ```name```)

#### _Phát bài hát dựa theo ```song_id``` hoặc ```url``` hoặc ```name``` của bài hát ( Stream từ server Javis):_
```sh
service: youtube_assistant.play_media
data:
  entity_id: media_player.audiocast_quang
  song_id: cfbNtHNCMBo
  url: https://www.youtube.com/watch?v=cfbNtHNCMBo
  name: chắc ai đó sẽ về
```      
##### _Ý nghĩa của các trường_
- ```entity_id```: entity_id của thiết bị phát
- ```song_id```: id của bài hát 
- ```url```: url của bài hát (nếu có cả 2 trường ```id``` và ```url``` sẽ ưu tiên trường ```id```)
- ```name```: name của bài hát (ưu tiên ```song_id``` > ```url``` > ```name```)
#### _Phát một playlist( Gọi trực tiếp từ server Javis):_
```sh
service: youtube_assistant.play_list
data:
  entity_id: media_player.audiocast_quang
  list_id: RDVWH3GDikM9M
  url: https://www.youtube.com/watch?v=VWH3GDikM9M&list=RDVWH3GDikM9M
```      
##### _Ý nghĩa của các trường_
- ```entity_id```: entity_id của thiết bị phát
- ```list_id```: id của playlist
- ```url```: url của playlist (nếu có cả 2 trường ```list_id``` và ```url``` sẽ ưu tiên trường ```list_id```)

#### _Phát một playlist( Stream từ server Javis):_
```sh
service: youtube_assistant.play_list_stream
data:
  entity_id: media_player.audiocast_quang
  list_id: RDVWH3GDikM9M
  url: https://www.youtube.com/watch?v=VWH3GDikM9M&list=RDVWH3GDikM9M
```      
##### _Ý nghĩa của các trường_
- ```entity_id```: entity_id của thiết bị phát
- ```list_id```: id của playlist
- ```url```: url của playlist (nếu có cả 2 trường ```list_id``` và ```url``` sẽ ưu tiên trường ```list_id```)


