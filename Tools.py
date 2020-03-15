import json
import time
import vk_api
import threading
from queue import Queue
from vk_api.exceptions import ApiError
from vk_api.longpoll import VkLongPoll, VkEventType
# User LongPoll dor VK 
def watch(q,token):
    ids = [562261850, 367916459]
    chat_name = 'тестирование'
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        try:
            print(event.raw, event.type,event.extra_values)
            if event.type == VkEventType.MESSAGE_NEW:
                if event.user_id not in ids:
                    if event.extra_values['source_act'] == 'chat_title_update' and event.extra_values['source_text'] != chat_name:
                        q.put(('t',event.chat_id,chat_name))
                    elif event.extra_values['source_act'] == 'chat_photo_update':
                        q.put(('p',event.chat_id))
                    elif event.extra_values['source_act'] == 'chat_pin_message':
                        q.put(('m',event.peer_id))
        except (KeyError, IndexError):
            pass
def do(q,token,k):
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    while True:
        data = q.get()
        print(data)
        type = data[0]
        id = data[1] - k
        try:
            if type == 't':
                vk.messages.editChat(chat_id=id, title=data[2])
            elif type == 'p':
                vk.messages.deleteChatPhoto(chat_id=id)
            elif type == 'm':
                vk.messages.unpin(peer_id=id)
        except ApiError as e:
            if 'flood control' in str(e):
                time.sleep(120)
            else:
                print(e)

def main():
    try:
        q = Queue()
        DataJson = [('...',562261850),('...',367916459)]
        w = DataJson[0]
        k = (0,-7)
        n = 0
        threading.Thread(target=watch,args=(q,w[0])).start()
        for x in DataJson:
            token = x[0]
            threading.Thread(target=do,args=(q,token,k[n])).start()
            n += 1
    except Exception as error:
        print("Произошла ошибка: ", error)
        pass
if __name__ == "__main__":
    main()




