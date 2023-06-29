import datetime
import os

import isodate as isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс для ютуб-плейлиста"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.response = PlayList.youtube.playlists().list(id=playlist_id,
                                                          part='snippet',
                                                          maxResults=50,
                                                          ).execute()
        try:
            self.title = self.response['items'][0]['snippet']['title']
            self.url = f'https://www.youtube.com/playlist?list={playlist_id}'
        except IndexError:
            raise ValueError('Incorrect playlist id. Please, try again.')

    @property
    def videos_response(self):
        """
        Возвращает список данных всех видео в плейлисте.
        """
        playlist_videos = PlayList.youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                                part='contentDetails',
                                                                maxResults=50,
                                                                ).execute()
        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                        id=','.join(video_ids)
                                                        ).execute()
        return video_response

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео в плейлисте (по количеству лайков).
        """
        best_video = {"id": "id", "likeCount": 0}
        for video in self.videos_response['items']:
            if int(video['statistics']['likeCount']) > best_video["likeCount"]:
                best_video["id"] = video["id"]
                best_video["likeCount"] = int(video['statistics']['likeCount'])
        return f"https://youtu.be/{best_video['id']}"

    @property
    def total_duration(self):
        """
        Возвращает объект класса datetime.timedelta с суммарной длительностью плейлиста.
        """
        total_duration = datetime.timedelta(seconds=0)
        for video in self.videos_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration
