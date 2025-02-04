import os

from googleapiclient.discovery import build


class Video:
    """
    Класс для ютуб-канала, который получает информацию о видео по его id
    """

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        self.video_id: str = video_id
        self.video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=video_id
                                                          ).execute()
        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.url: str = f'https://www.youtube.com/watch?v={self.video_id}'
        self.views_count: str = self.video_response['items'][0]['statistics']['viewCount']
        self.likes_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """
        Выводит название канала для пользователей
        """
        return self.video_title


class PLVideo(Video):
    """
    Дочерний класс(Video) для ютуб-канала, который получает информацию плейлисте по его id, а также всю информацию
    родительского класса
    """
    def __init__(self, video_id: str, playlist_id):
        super().__init__(video_id)
        self.playlist_id: str = playlist_id
        self.playlist_videos = Video.youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()
