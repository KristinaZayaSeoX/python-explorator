import vk_api
import requests
import threading
from sys import exit
from os import chdir
from time import sleep
from random import randint

v = 5.90 #-- API current version
chdir('D:\VK-Photos') # -- working directory for save photos
f = open('token.txt') #-- token file
token =  [line for line in f.readlines()] #-- valid VK token
user_id = 558288024 #-- target user_id

class Download_Photos(object):
    def __init__(self, offset):
        self.access_token = token
        self.user_id =  user_id
        self.name = 'photo'
        self.offset = offset

    @staticmethod
    def Download(file_name, content):  # Создаем функцию-загрузчик
        with open(file_name, 'ab+') as file:
            file.write(content)

    def Main_thread(self):
        vk_session = vk_api.VkApi(token=self.access_token)
        self.vk = vk_session.get_api()
        get_photo = self.vk.photos.get(count=200, owner_id=user_id, offset=self.offset, album_id='saved', v=v)  # запрос к API
        self.response = get_photo['items']
        photo_list = []
        for self.x in self.response:
            url = self.x['photo_604']  # --ПОЛУЧАЕМ ССЫЛКИ
            photo_list.append(url)  # --ЗАПОЛНЯЕМ СПИСОК ССЫЛКАМИ
        try:
            for self.URL in photo_list:  # создаем цикл запросов
                r = requests.get(self.URL, stream=True)  # ==ОТПРАВЛЯЕМ ЗАПРОС ПО КАЖДОЙ ССЫЛКЕ
                if r.status_code == 200:  # -- ЕСЛИ ВСЕ В ПОРЯДКЕ ТО..
                   name = self.name + str(randint(1,12000))
                   self.Download(name + '.jpg', r.content)  # -- ЗАГРУЖАЕМ ВСЕ СЕБЕ В ПАПКУ
                   sleep(1)  # -- устанавливаем интервал в одну секунду
        except FileExistsError:
            pass
'''
Скачиваем нужное количество фотографий
к себе на компьютер
'''
x = Download_Photos
offset_list = [x*200 for x in range(30)]
try:
  for i in offset_list:
    x.Main_thread(Download_Photos(i)).start()
except Exception as error:
    print('Скачивание остановлено по причине ошибки: {}'.format(error))
    exit(0)
