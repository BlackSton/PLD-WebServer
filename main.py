# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 22:27:24 2021

@author: rltjr
"""

import client_laser
import client_server
from time import sleep
from flask import Flask,render_template
app = Flask(__name__)
@app.route('/')
def home():
    try :
        PLD1_v = data["PLD1"]["vaccum"]["listen"][0].split(',')[-1][1:]
    except:
        PLD1_v = "-"
    try :
        PLD2_v = data["PLD2"]["vaccum"]["listen"][0].split(',')[-1][1:]
    except:
        PLD2_v = "-"
    return render_template("home.html",
                           PLD1= PLD1_v,
                           PLD2= PLD2_v,
                           LASER=data["LASER_COMMAND"])

def load_setting(): #load setting.ini and load ip and port
    try:
        f = open('setting.ini','r')
    except:
        f = open('setting.ini','w')
        f.close()
        f = open('setting.ini','r')
    lines = f.readlines()
    f.close()
    for line in lines:
        if line[-1] == '\n':
            line = line[:-1]
        temp = line.split('=')
        data[temp[0]] = temp[1]
            
if __name__ == "__main__":
    data = {"PLD1":{"temp"   :{"listen":[],"result":{},'port':'none'}, # Devices Data LINE
                      "vaccum" :{"listen":[],"result":{},'port':'none'},
                      "laser"  :{"listen":[],"result":{},'port':'none'},
                      "stepper":{"listen":[],"result":{},'port':'none'}},
            "PLD2":{"temp"   :{"listen":[],"result":{},'port':'none'}, # Devices Data LINE
                      "vaccum" :{"listen":[],"result":{},'port':'none'},
                      "laser"  :{"listen":[],"result":{},'port':'none'},
                      "stepper":{"listen":[],"result":{},'port':'none'}},
        "LASER":"", #"LASER": Received Data from LASER SERVER
        'SERVER_INTERVAL':0.5,'SERVER_state':False, #client setting
        'LASER_INTERVAL':0.5,"LASER_state":False,   #Laser  setting      
        "Microstep":800,                                       #stepper setting
        "stop":True,                                           #Superlatttice setting
        "STATE":[]                 
        ,"LASER_COMMAND":{"listen":[]}                            #STATE line Data
        }
    tcp_laser  = client_laser.tcp(data)
    PLD1 =       client_server.tcp(data,1)
    PLD2 =       client_server.tcp(data,2)
    class_value = {'LASER_tcp':tcp_laser}
    load_setting()
    tcp_laser.connect()
    PLD1.connect()
    PLD2.connect()
    app.run(host="0.0.0.0",port=80,debug=True)
    input("exit")
    tcp_laser.close()
    PLD1.close()
    PLD1.close()
    