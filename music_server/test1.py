import requests
#api play
def test_play(media_id, song_id, number = 0, repeat = False , version = 1):
    url = 'http://localhost:2024/media/play'
    data = {
        "media_id": media_id,
        "song_id": song_id,
        "url": "",
        "name": "",
        "repeat": repeat,
        "number": number,
        "version": version
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200

def test_play_playlist(media_id,list_id,  version = 1):
    url = 'http://localhost:2024/media/play_playlist'
    data = {
        "media_id": media_id,
        "list_id": list_id,
        "url": "",
        "version": version
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200

def test_next(media_id):
    url = 'http://localhost:2024/media/next'
    data = {
        "media_id": media_id
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200

def test_previous(media_id):
    url = 'http://localhost:2024/media/previous'
    data = {
        "media_id": media_id
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200

media_id_1 = "media_player.loa_da_vung_tran_2"
media_id_2 = "media_player.da_vung_69"
media_id_3 = "media_player.googlehome0056"
version = 1
number = 5
repeat = False
list_id = "RDDgI_Lgv2To0"
list_song_id = ["S2JAeuwjeN4", "IMRdRGWXHnU", "RBQ-IoHfimQ", "i0avdvFMghs"]

# 1. Test play a song, a media (oke)
# test_play(media_id_1,list_song_id[0])
# 2. Test play a song 2 media (oke)
# test_play(media_id_1,list_song_id[0])
# test_play(media_id_2, song_id=list_song_id[0])
# 3. Test play a playlist, a media (testing)
# test_play(media_id_1,list_song_id[0], number, repeat)
# 4. Test play a playlist, 2 media (todo)
# test_play(media_id_1,list_song_id[2], number, repeat)
# test_play(media_id_3,list_song_id[2], number, repeat)
# # 5. Test play next song a media (todo)
# test_play(media_id_1,list_song_id[3], number, repeat)
test_next(media_id_1)
# 6. Test previous song a media (todo)
# test_play(media_id_1,list_song_id[3], number, repeat, version)
# test_previous(media_id_1)
# 7. Test_playlist
# test_play_playlist(media_id_1, list_id, version)
