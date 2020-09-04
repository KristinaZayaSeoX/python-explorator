# -*- coding: utf-8 -*-
import requests
import random
from bs4 import BeautifulSoup
from os import chdir
from time import sleep
from sys import exit
from threading import Thread

class Req:
    def __init__(self, url, params = None):
        self.url = url
        self.params = params
        self.timeout = 0
      
    def get_response(self):
        try:
            self.response = requests.get(self.url, params=self.params)
            if self.response.status_code == 200:
               print(f'server status: {self.response.status_code}')
               return self.response
            else:
               print('error!')
        except Exception as ems:
               print(ems)
               pass
    
    @staticmethod
    def sleep_time(value):
        tsl = sleep(value)
        if isinstance(value,int) == True:
            return tsl
    
    def print_info(self):
        content = self.get_response
        print(f'получены данные: {content()}')
#----------------------------------------------------#
chdir('D:\Coding Python')
token_file = open('token.txt')
token = [line for line in token_file.readlines()]
random_id = 0
Chat_Id = 161
v = 5.103
user_bot = 537298000
s = '💬'
Info = '💬Привет! Я - ботиха Кристины. ✍🏻Мои команды: --story, --anime, --pozor, --help me  Мой функционал постепенно улучшается, обо всех изменениях вы можете узнать у моей создательницы *id530720952 (Кристины)✅ '
#----------------------------------------------------#
class VKBot_Interface:
    def __init__(self, method, params):
        self.url = 'https://api.vk.com/method/'
        self.method = method
        self.params = params
        self.msg = ' done!'

    def get_vk(self):
        self.request = f'{self.url}{self.method}/'
        sleep(0.55)
        self.response = Req.get_response(Req(self.request,params=self.params))
        return self.response.json()

    def print_info(self):
        content = self.get_vk()
        self.ms = f'результат запроса к API: {content} '+ self.msg
        print(self.ms)
        return self.ms


class NewReqTestBS(Req):
    def __init__(self):
        self.url = 'https://istoriipro.ru/'
        super().__init__(self.url)

    def response_get(self,url,params):
        self._response = super().get_response()
        return self._response

    def print_info(self):
        response = self.response_get(self.url, None)
        print(f'{response}\nplease parse data..')
    
    def get_bs4(self):
        response = self.response_get(self.url, None)
        bs = BeautifulSoup(response.text, 'html.parser')
        self.sleep_time(1)
        find_dv = bs.find_all('a', {'class':'continue-reading-link'})
        self.data = []
        for row in find_dv:
            result = row['href']
            self.data.append(result)
        return self.data

#= ==============================================================#
req = Req
vk = VKBot_Interface
info = Req.print_info
bs = NewReqTestBS
chat_param = {'access_token':token, 'count':1, 'v':v}
rand_link = NewReqTestBS.get_bs4(NewReqTestBS())
response = vk.get_vk(VKBot_Interface('photos.get',{'access_token':token,'owner_id':537298000, 'album_id':274728700, 'count':200, 'v':v}))
result = response['response']['items']
photos = []
for x in result:
    pid = x['id']
    photo_attachment = (f'photo{user_bot}_{pid}')
    photos.append(photo_attachment)
#================================================================#
def VK_Post():
    response = vk.get_vk(VKBot_Interface('wall.get',{'access_token':token,'owner_id':-152433395,'count':10, 'filter':'owner', 'v':v}))
    owner = -152433395
    result = response['response']['items']
    post_list = []
    for items in result:
        for key, value in items.items():
            if key == 'id':
                attachments = f'wall{owner}_{value}'
                post_list.append(attachments)
    result_post_list = post_list[1:]
    return result_post_list

def VK_Bot():
    message_id = ''
    while True:
      try:
          response = vk.get_vk(VKBot_Interface('messages.getConversations',chat_param))
          print(response)
          sleep(0.55)
          items = response['response']['items']
          chat_id = items[0]['conversation']['peer']['local_id']
          last_message_id = items[0]['conversation']['last_message_id']
          for x in items:
             ID = x['conversation']['last_message_id']
             if ID != message_id:
                message_id = last_message_id
                text = x['last_message']['text']
                user = x['last_message']['from_id']
                config = [
                 {'access_token':token,'chat_id':chat_id,'message':random.choice(rand_link),'random_id':0,'v':v},
                 {'access_token':token,'chat_id':chat_id,'attachment':random.choice(photos),'random_id':0,'v':v},
                 {'access_token':token,'chat_id':chat_id,'message':Info,'random_id':0,'v':v},
                 {'access_token':token,'chat_id':chat_id,'attachment':random.choice(VK_Post()),'random_id':0,'v':v},
                 {'access_token':token,'chat_id':chat_id,'message':'testyrovanye 1.4','random_id':0,'v':v},
                 {'access_token':token,'chat_id':chat_id,'message':'testyrovanye 1.5','random_id':0,'v':v},
                 {'access_token':token,'chat_id':chat_id,'message':'testyrovanye 1.6','random_id':0,'v':v}
                         ]
                commands = {
                  'vk_api1':VKBot_Interface('messages.send',config[0]),
                  'vk_api2':VKBot_Interface('messages.send',config[1]),
                  'vk_api3':VKBot_Interface('messages.send',config[2]),
                  'vk_api4':VKBot_Interface('messages.send',config[3]),
                  'vk_api5':VKBot_Interface('messages.send',config[4]),
                  'vk_api6':VKBot_Interface('messages.send',config[5]),
                  'vk_api7':VKBot_Interface('messages.send',config[6])
                           }
                command_config = [('--story',commands['vk_api1']),('--anime',commands['vk_api2']),('--info',commands['vk_api3']),('--pozor',commands['vk_api4'])]
                for x in command_config:
                    command = x[0]
                    execute = x[1]
                    if text == command and user != user_bot:
                        vk.get_vk(execute)
      except Exception as ems:
         print('error: ', ems)
         exit(0)

class TeleBot_Interface:
    def __init__(self):
        self.token = '' # Поставить сюда токен своего телеграм-бота
        self.bot_auth = 'bot' + self.token
        self.API_link = f'https://api.telegram.org/{self.bot_auth}/'
        self.Update_Link = f'{self.API_link}getUpdates?offset=-1'

    def updates_get(self):
        response = req.get_response(Req(self.Update_Link))
        return response.json()
    
    def send_message(self,chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.API_link + 'sendMessage', data=params)
        return response

    def bot_polling(self):
        while True:
            self.update = self.updates_get()
            print(self.update)
            sleep(3)
            self.update_id = self.update['result'][0]['update_id']
            self.new_update_id = self.updates_get()['result'][0]['update_id']
            if self.new_update_id != self.update_id:
                print('/get updates')
                try:
                    message_source = self.updates_get()['result'][0]['message']
                    chat_id = message_source['chat']['id']
                    message_text = message_source['text']
                    self.send_message(chat_id,message_text)
                except (KeyError, IndexError):
                    pass
def TeleBot():
    try:
        t_bot = TeleBot_Interface()
        t_bot.bot_polling()
    except requests.ConnectionError:
        exit(0)

threads = {'t1':Thread(target=TeleBot), 't2':Thread(target=VK_Bot)}   
for key,thread in threads.items():
    thread.start()


