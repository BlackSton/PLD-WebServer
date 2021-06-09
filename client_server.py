# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:59:46 2021

@author: rltjr
"""

from threading import Thread,active_count
from time import sleep
import socket

class tcp():
    def __init__(self,data,mode):
        self.data = data
        self.mode = mode
        self.stop = False
        self.class_value = {}
        self.listen_keyword = "listen$"
        self.last_word = '$'
    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            print("Server connect to %s:%s"
                                      %(self.data['SERVER_IP'+str(self.mode)],self.data['SERVER_PORT'+str(self.mode)]))
            self.stop = False
            self.client_socket.connect((self.data['SERVER_IP'+str(self.mode)], int(self.data['SERVER_PORT'+str(self.mode)]))) 
            self.th_r = Thread(target=self.reading)
            self.th_l = Thread(target=self.listen)
            self.th_r.start()
            self.th_l.start()
            self.data['SERVER_state'] = True
            print("Server Connected")
            return True
        except:
            print("connection fail!")
            return False
    def count(self):
        print(active_count())
    def close(self):
        self.stop = True
        self.data['SERVER_state'] = False
        try:
            self.client_socket.close()
            self.th_l.join()
            self.th_r.join()
        except:
            print("server was already closed...")
            pass
        print("disconnected...")
    def send(self,command):
        try:
            self.client_socket.send((command+self.last_word).encode('utf-8'))
        except:
            pass
    def listen(self):
        while self.stop == False:
            try:
                self.client_socket.send(self.listen_keyword.encode('utf-8'))
            except:
                print("sending has problem!")
                self.data['SERVER_state'] = False
                self.stop = True
                pass
            sleep(self.data['SERVER_INTERVAL'])

    def reading(self,):
        buffer = ""
        while self.stop == False:
            try:
                receive = self.client_socket.recv(1024).decode('utf-8')
            except:
                print("receiving error")
            try:
                receive[0]
                buffer = buffer + receive
            except:
                self.data['SERVER_state'] = False
                self.stop = True
                break
            if buffer[-1] == '$':
                buffer = buffer[:-1]
                if buffer[-1] == '\n':
                    devices = buffer[:-1].split('\n')
                    for device in devices:
                        temp = device.split('\t')
                        device_name    = temp[0]
                        device_port    = temp[-1]
                        device_command = temp[1:-1]
                        try:
                            self.data["PLD"+str(self.mode)][device_name]["listen"] = device_command
                            self.data["PLD"+str(self.mode)][device_name]["port"]   = device_port
                        except:
                            pass
                else:
                    print(buffer.encode('utf-8'))
                buffer = ""