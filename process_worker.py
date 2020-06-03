# -*- coding: utf-8 -*-

import subprocess
import os
import time
import psutil
from sys import exit
dirname = 'some path to working directory'
help_msg = 'for more information print -help\n for exit print exit\n for kill process enter process id..'
help_menu = ['p -start => process start','p -chdir => change directory','p -ldir => viewing content of directory','p -list => create list of active processes']
print(help_msg)              

class Subpro:
    def __init__(self,file,*args):
        self.file = file
        self.start_cwd = dirname
        
    def __start__(self):
        self.pro = subprocess.Popen(self.file)
    
    def get_PID(self):
        self.PID = self.pro.pid
        return self.PID
    
    @staticmethod
    def get_system_pro_list():
        ps_list = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name'])
            except psutil.NoSuchProcess:
                exit(0)
            else:
                print(pinfo)
                time.sleep(0.1)
        ps_list.append(pinfo)
        print(ps_list)
    
    def kill_pro(self):
        try:
            self.pro.kill()
        except Exception as e:
            print(e)
            pass
        
    def kill_pro_by_ID(self,_id):
        try:
            self._id = _id
            os.system('taskkill /PID {}'.format(self._id))
        except Exception as e:
            print(e)
            pass
    
    def change_directory(self,_DIR):
        try:
           os.chdir(_DIR)
        except FileNotFoundError:
           print('Неверное имя директории...')
           pass
       
    @staticmethod
    def print_help():
      for x in help_menu:
        print(x)
        time.sleep(0.25)
        
    @staticmethod
    def kill_group_pro(name_pro):
        ps_list = []
        for proc in psutil.process_iter():
             try:
                pinfo = proc.as_dict(attrs=['pid', 'name'])
             except psutil.NoSuchProcess:
                 pass 
             else:
                 print(pinfo)
                 time.sleep(0.1)
             ps_list.append(pinfo) 
        prs = []
        for x in ps_list:
            p_name = x['name']
            pid = x['pid']
            if p_name == str(name_pro):
                prs.append(pid)
            else:
                pass
            print(prs)    
        for x in prs:
           try:
              p = psutil.Process(x)
              p.terminate()
           except psutil.Error as error_message:
              print(error_message)
              exit(0)   
                 
    def get_file_listdir(self):
        _cwd = os.getcwd()
        if _cwd != self.start_cwd:
            print(os.listdir(_cwd))
        else:
            pass
commands = ['p -ldir','-help','exit']
def main():
    while True:
        try:
             q = Subpro
             p = Subpro(None)
             i = input('enter command..')
             command = i.split('/')
             if command[0] == 'p -start':
                proccess = command[1]
                q.__start__(Subpro(proccess))
             if command[0] == 'p -chdir':
                chdir = command[1]
                q.change_directory(Subpro,chdir)
             if i == 'p -ldir':
                q.get_file_listdir(Subpro(None)) 
             if i == 'p -list':
                q.get_system_pro_list()
             if i == '-help':
                q.print_help()
             if i == 'exit':
                 exit(0)
             if i != False and type(i) != int and i not in commands and len(str(i)) > 5:
               try:
                  q.kill_group_pro(i)
               except Exception:
                   pass
             elif i != False and int(i) > 0:
                p.kill_pro_by_ID(int(i))
             else:
                pass
        except (ValueError, OSError):
            pass            
if __name__ == '__main__':
    main()
