# -*- coding: utf-8 -*-

from __future__ import division
import RPIO as G
from time import sleep, time
import datetime
from random import randint
import math

G.setmode(G.BCM)
G.setwarnings(False)

pins = [17,27,22]

for pin in pins:
    G.setup(pin, G.OUT)

from shift import Sipo_reg


reg = Sipo_reg([2, 3, 4], 2)
# column, rows

values = {
        "0" : [1,1,1,1,1,1,0],
        "1" : [0,1,1,0,0,0,0],
        "2" : [1,1,0,1,1,0,1],
        "3" : [1,1,1,1,0,0,1],
        "4" : [0,1,1,0,0,1,1],
        "5" : [1,0,1,1,0,1,1],
        "6" : [1,0,1,1,1,1,1],
        "7" : [1,1,1,0,0,0,0],
        "8" : [1,1,1,1,1,1,1],
        "9" : [1,1,1,1,0,1,1],
        " " : [0,0,0,0,0,0,0]
    }

def loop():
    def capacity():   
        
        res = []
        
        def times(gpio_id, val):
            if len(res) < 6:
                res.append(int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 10000))
                print("Pridano")
            else: 
                G.stop_waiting_for_interrupts()

        G.add_interrupt_callback(7, times, edge="rising")

        G.wait_for_interrupts()

        diff_list = []

        for i in range(3):
            diff_list.append(res[i + 1] - res[i]) 

        diff = reduce(lambda x, y: x + y, diff_list) / len(diff_list)
        tl = diff * 0.33
        number = (tl / 10000) / 693
        prefixes = {
            "0" : 10**3, 
            "1" : 10**6, 
            "2" :10**9
        }

        for key, value in prefixes.iteritems():
            if number * value > 1 and number * value < 1000:
                return (number * value, key)


    arr = []
    ret_val, key = capacity()

    for i in str(int(ret_val)):
        arr.append(i)

    if len(arr) == 2:
        arr.insert(0, 0)
    elif len(arr) == 1:
        arr.insert(0, 0)
        arr.insert(1, 0)

    timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)

    while int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000) < timestamp + 10000:
        G.output(pins[int(key)], 1)

        enable = [1,0,0]
        reg.shift_out(values[str(arr[0])] + [0] + enable + [0] * 5) 
        sleep(0.005)
        reg.clear() 
            
        enable = [0,1,0]
        reg.shift_out(values[str(arr[1])] + [0] + enable + [0] * 5) 
        sleep(0.005)
        reg.clear() 
            
        enable = [0,0,1]
        reg.shift_out(values[str(arr[2])] + [0] + enable + [0] * 5) 
        sleep(0.005)
        reg.clear() 
         
    for pin in pins:
        G.output(pin, 0)    

loop()

    