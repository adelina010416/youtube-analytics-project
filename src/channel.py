import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__id = channel_id
        channel = self.get_service().channels().list(id=self.__id, part='snippet,statistics').execute()
        try:
            self.title = channel['items'][0]['snippet']['title']
            self.description = channel['items'][0]['snippet']['description']
            self.url = 'https://www.youtube.com/channel/' + self.__id
            self.subscribers = channel['items'][0]['statistics']['subscriberCount']
            self.video_count = channel['items'][0]['statistics']['videoCount']
            self.views = channel['items'][0]['statistics']['viewCount']
        except KeyError or IndexError:
            raise Exception('DataNotFound: try another chanel id')

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscribers) + int(other.subscribers)

    def __sub__(self, other):
        return int(self.subscribers) - int(other.subscribers)

    def __lt__(self, other):
        return int(self.subscribers) < int(other.subscribers)

    def __le__(self, other):
        return int(self.subscribers) <= int(other.subscribers)

    def __gt__(self, other):
        return int(self.subscribers) > int(other.subscribers)

    def __ge__(self, other):
        return int(self.subscribers) >= int(other.subscribers)

    def __eq__(self, other):
        return int(self.subscribers) == int(other.subscribers)

    @property
    def id(self):
        return self.__id

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.__id, part='snippet,statistics').execute()
        info = json.dumps(channel, indent=4, ensure_ascii=False)
        return info

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с API"""
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, file_name: str):
        """Записывает статистику канала в .json файл."""
        try:
            extension = file_name.split('.')
            if extension[-1] != 'json':
                raise ValueError('Please, use ".json" as extension')
            if extension[1] == '' or extension[0] == '':
                raise ValueError("Please, state file name and it's extension: name.json")
        except IndexError:
            raise ValueError("Please, state file name and it's extension: name.json")

        with open(file_name, 'w', encoding='utf-8') as file:
            data = {
                'title': self.title,
                'chanel_id': self.__id,
                'description': self.description,
                'url': self.url,
                'subscribers_count': self.subscribers,
                'video_count': self.video_count,
                'views_count': self.views
            }
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
