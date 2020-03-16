import vk_api
import requests
import threading
from sys import exit
from os import chdir
from time import sleep

v = 5.90 #-- API current version
chdir('D:\VK-Photos') # -- working directory for save photos
f = open('token.txt') #-- token file
token =  [line for line in f.readlines()] #-- valid VK token
user_id = 503476215 #-- target user_id

class Download_Photos(object):
    def __init__(self, offset):
        self.offset = offset
        self.access_token = token
        self.user_id =  user_id
        self.name = 'photo'
        self.num = 0
        self.max_count = 6000

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
                    while self.num <= self.max_count:
                        self.num+=1
                        self.name = self.name + str(self.num)
                        self.Download(self.name + '.jpg', r.content)  # -- ЗАГРУЖАЕМ ВСЕ СЕБЕ В ПАПКУ
                        sleep(1)  # -- устанавливаем интервал в одну секунду
        except FileExistsError:
            pass
'''
Скачиваем нужное количество фотографий
к себе на компьютер
'''
def main():
  t = Download_Photos
  try:
   max_count = 6000
   i = 0
   while i <= max_count:
       i += 200
       thread = t.Main_thread(Download_Photos(i))
       threads = threading.Thread(target=thread)
       threads.start()
  except Exception as e:
      print('Error!:{} Please,try again...').format(e)
      pass
if __name__ == "__main__":
    main()
