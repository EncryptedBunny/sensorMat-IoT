
# -*- coding: utf-8 -*-

# Mapping for Soundmat to 3x3 Matrix
# q(4,8), w(3), e(1,2), a(11,12), s(7,10), d(5,6), z(15,16), x(14), c(9,13)

import socket
import sys
import os
import struct
import numpy as np
import pandas as pd
from array import array
from _ctypes import Array
import csv
import json
import argparse
import random
import time
import threading

# OSC
from pythonosc import udp_client

# MQTT
import paho.mqtt.client as mqtt

# MQTT Setup
MQTT_Client = "test.mosquitto.org"
MQTT_Port = 1883
MQTT_Topic ="/sound_demo/data/#"

# OSC Setup
ip = "10.30.11.36"
port = 12003

#ip = "127.0.0.1"
#port = 5005

# Make client channels to send packets.
OSCclient = udp_client.SimpleUDPClient(ip, port)

# Time out setup
reset_time = 10.0

def reset_mat():
    global var_q,var_w,var_e,var_a,var_s,var_d,var_z,var_x,var_c

    OSCclient.send_message("/q", 0)
    OSCclient.send_message("/w", 0)
    OSCclient.send_message("/e", 0)
    OSCclient.send_message("/a", 0)
    OSCclient.send_message("/s", 0)
    OSCclient.send_message("/d", 0)
    OSCclient.send_message("/z", 0)
    OSCclient.send_message("/x", 0)
    OSCclient.send_message("/c", 0)

    var_q = 0
    var_w = 0
    var_e = 0
    var_a = 0
    var_s = 0
    var_d = 0
    var_z = 0
    var_x = 0
    var_c = 0

    set_timer()


def set_timer():
    global timer

    timer = threading.Timer(reset_time, reset_mat)
    timer.start()

def reset_timer():
    
    global timer

    timer.cancel()
    timer = threading.Timer(reset_time, reset_mat)
    timer.start()

# Start timer
set_timer()

# Globals
position_buf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

var_q = 0
var_w = 0
var_e = 0
var_a = 0
var_s = 0
var_d = 0
var_z = 0
var_x = 0
var_c = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    global f 

    filename = "./Data_Dump/matMQTTData-%s" %str(time.time()).replace(".","-")

    f = open(filename, 'wb+')
       
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_Topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    
    global position_buf
    global var_q, var_w, var_e, var_a, var_s, var_d, var_z, var_x, var_c

    q,w,e,a,s,d,z,x,c = [0,0,0,0,0,0,0,0,0]

    data = msg.payload

    new_str = data.decode('utf-8') # Decode using the utf-8 encoding

    dt = json.loads(new_str)

    f.write(data)
    f.flush()

    reset_timer()

    if position_buf == dt['Occupancy']:
        None
    else:
        position_buf = dt['Occupancy']
        print(position_buf)

        b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16 = position_buf

        if (b4 or b8):
            q = 1
        if (b3):
            w = 1
        if (b1 or b2):
            e = 1
        if (b11 or b12):
            a = 1
        if (b7 or b10):
            s = 1
        if (b5 or b6):
            d = 1
        if (b15 or b16):
            z = 1
        if (b14):
            x = 1
        if (b9 or b13):
            c = 1

        if (var_q != q):
            var_q = q
            OSCclient.send_message("/q", var_q)
        if (var_w != w):
            var_w = w
            OSCclient.send_message("/w", var_w)
        if (var_e != e):
            var_e = e
            OSCclient.send_message("/e", var_e)
        if (var_a != a):
            var_a = a
            OSCclient.send_message("/a", var_a)
        if (var_s != s):
            var_s = s
            OSCclient.send_message("/s", var_s)
        if (var_d != d):
            var_d = d
            OSCclient.send_message("/d", var_d)
        if (var_z != z):
            var_z = z
            OSCclient.send_message("/z", var_z)
        if (var_x != x):
            var_x = x
            OSCclient.send_message("/x", var_x)
        if (var_c != c):
            var_c = c
            OSCclient.send_message("/c", var_c)

        
# Initialise MQTT 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_Client, MQTT_Port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.loop_forever()
f.close()