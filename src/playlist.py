import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build


class MixinPL:
    """
    Миксин для работы с API.
    """

    api_key: str = os.getenv('YT_API_KEY')

    @staticmethod
    def get_build():
        """
        Метод для получения специального объекта для работы с API
        """
        youtube = build('youtube', 'v3', developerKey=MixinPL.api_key)
        return youtube


class PlayList(MixinPL):
    """
    Класс для работы с плейлистом ютуба.
    """

    def __init__(self, playlist_id: str):
        self.playlist_id: str = playlist_id

        self.playlist_info = self.get_build().playlists().list(id=self.playlist_id, part='contentDetails,snippet',
                                                               maxResults=50,
                                                               ).execute()
        self.playlist_videos = self.get_build().playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.v_response = self.get_build().videos().list(part='statistics,contentDetails',
                                                         id=','.join(self.video_ids)
                                                         ).execute()

        self.title: str = self.playlist_info['items'][0]['snippet']['title']
        self.url: str = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self) -> timedelta:
        """
        Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """

        playlist_duration = timedelta(0)

        # итерация по видео из плейлиста
        for video in self.v_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            playlist_duration += duration

        return playlist_duration

    def show_best_video(self) -> str:
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """

        more_likes = sorted(self.v_response['items'], key=lambda el: el['statistics']['likeCount'], reverse=True)
        return f'https://youtu.be/{more_likes[0]["id"]}'
