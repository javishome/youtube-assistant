# Service youtube assistant cho phép phát bài hát youtube dựa trên từ khóa

### Khai báo trong configuration.yaml như sau:

```sh
youtube_assistant:
```   
### Khai báo gọi dịch vụ như sau:
#### _Phát bài hát dựa theo ```tên``` hoặc ```url``` hoặc ```id```:_
```sh
service: youtube_assistant.play_song
data:
  entity_id: media_player.audiocast_quang
  name: chắc ai đó sẽ về
  id: cfbNtHNCMBo
  url: https://www.youtube.com/watch?v=cfbNtHNCMBo
  number: 10
```      
##### _Ý nghĩa của các trường_
- ```entity_id```: entity_id của thiết bị phát
- ```name```: tên của bài hát 
- ```id```: id của bài hát 
- ```url```: url của bài hát (nếu có cả 2 trường ```id``` và ```url``` sẽ ưu tiên trường ```id```)
- ```number```: số lượng bài hát liên quan muốn phát (không bắt buộc có trường này) mặc định là 5
Chú ý chỉ cần điền 1 trong các trường name, id và url
#### _Phát một playlist:_
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
##### Phát một playlist:

```sh
service: youtube_assistant.play_list
data:
  entity_id: media_player.audiocast_quang
  list_id: RDVWH3GDikM9M
```
```component``` sẽ tìm kiếm ```id``` tất cả các bài hát trong list, phát bài đầu tiên và đưa tất cả các bài còn lại vào queue. Có thể dùng trường ```url``` thay cho trường ```list_id``` và copy cả link của playlist:
```sh
  url: https://www.youtube.com/watch?v=VWH3GDikM9M&list=RDVWH3GDikM9M
```


