import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.sub_count = int(self.channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.views_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        """
        Возвращает информацию для пользователей "название канала(ссылка на канал)".
        """
        return f'{self.title}({self.url})'

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API.
        """
        return cls.youtube

    def to_json(self, path):
        """
        Сохраняет в файл значения атрибутов экземпляра Channel.
        """
        with open(path, 'w') as f:
            data = self.__dict__
            del data['channel']
            json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

    def __add__(self, other):
        """
        Складывает количество подписчиков двух каналов и
        возвращает общее количество подписчиков.
        """
        return self.sub_count + other.sub_count

    def __sub__(self, other):
        """
        Возвращает разницу подписчиков двух каналов.
        """
        return self.sub_count - other.sub_count

    def __gt__(self, other):
        """
        Возвращает результат (True/False) сравнения ">" количества подписчиков на каналах.
        """
        return self.sub_count > other.sub_count

    def __ge__(self, other):
        """
        Возвращает результат (True/False) сравнения ">=" количества подписчиков на каналах.
        """
        return self.sub_count >= other.sub_count

    def __lt__(self, other):
        """
        Возвращает результат (True/False) сравнения "<" количества подписчиков на каналах.
        """
        return self.sub_count < other.sub_count

    def __le__(self, other):
        """
        Возвращает результат (True/False) сравнения "<=" количества подписчиков на каналах.
        """
        return self.sub_count <= other.sub_count

    def __eq__(self, other):
        """
        Возвращает результат (True/False) сравнения "==" количества подписчиков на каналах.
        """
        return self.sub_count == other.sub_count
