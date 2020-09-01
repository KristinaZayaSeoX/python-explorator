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
            self.response = requests.get(self.url)
            if self.response.status_code == 200:
               print(self.response.status_code)
               return self.response.content
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
url = 'https://api.vk.com/method/'
random_id = 0
Chat_Id = 161
v = 5.103
user_bot = 537298000
s = '💬'
Info = '💬Привет! Я - ботиха Кристины. ✍🏻Мои команды: --story, --anime, --pozor, --help me  Мой функционал постепенно улучшается, обо всех изменениях вы можете узнать у моей создательницы *id530720952 (Кристины)✅ '
#----------------------------------------------------#
class GetVK(Req):
    def __init__(self, method, params):
        self.url = url
        self.method = method
        self.params = params
        self.msg = ' done!'

    def get_vk(self):
        self.request = f'{self.url}{self.method}/'
        self.sleep_time(0.55)
        self.response = requests.get(self.request,params=self.params)
        return self.response.json()

    def print_info(self):
        content = self.get_vk()
        self.ms = f'результат запроса к API: {content} '+ self.msg
        print(self.ms)
        return self.ms

#GetVK.print_info(GetVK('messages.send',configs[3])) #---example request---#

class NewReqTestBS(Req):
    def __init__(self):
        self.url = 'https://istoriipro.ru/'

    def response_get(self):
        self._response = super().get_response()
        return self._response

    def print_info(self):
        response = self.response_get()
        print(f'{response}\nplease parse data..')
    
    def get_bs4(self):
        response = requests.get(self.url)
        bs = BeautifulSoup(response.text, 'html.parser')
        self.sleep_time(1)
        find_dv = bs.find_all('a', {'class':'continue-reading-link'})
        self.data = []
        for row in find_dv:
            result = row['href']
            self.data.append(result)
        return self.data
#==========================================#
req = Req
vk = GetVK
info = Req.print_info
bs = NewReqTestBS
chat_param = {'access_token':token, 'count':1, 'v':v}
rand_link = NewReqTestBS.get_bs4(NewReqTestBS())
response = vk.get_vk(GetVK('photos.get',{'access_token':token,'owner_id':537298000, 'album_id':274728700, 'count':200, 'v':v}))
result = response['response']['items']
photos = []
for x in result:
    pid = x['id']
    photo_attachment = (f'photo{user_bot}_{pid}')
    photos.append(photo_attachment)
#==========================================#
def VK_Post():
    response = vk.get_vk(GetVK('wall.get',{'access_token':token,'owner_id':-152433395,'count':10, 'filter':'owner', 'v':v}))
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

def Main():
    message_id = ''
    while True:
      try:
          response = vk.get_vk(GetVK('messages.getConversations',chat_param))
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
                 {'access_token':token,'chat_id':chat_id,'message':'testyrovanye 1.6','random_id':0,'v':v}]
                commands = {
                 'vk_api1':GetVK('messages.send',config[0]),
                  'vk_api2':GetVK('messages.send',config[1]),
                  'vk_api3':GetVK('messages.send',config[2]),
                  'vk_api4':GetVK('messages.send',config[3]),
                  'vk_api5':GetVK('messages.send',config[4]),
                  'vk_api6':GetVK('messages.send',config[5]),
                  'vk_api7':GetVK('messages.send',config[6])}
                command_config = [('--story',commands['vk_api1']),('--anime',commands['vk_api2']),('--info',commands['vk_api3']),('--pozor',commands['vk_api4'])]
                for x in command_config:
                    command = x[0]
                    execute = x[1]
                    if text == command and user != user_bot:
                        vk.get_vk(execute)
      except Exception as ems:
         print('error: ', ems)
         exit(0)
Thread(target=Main).start()



