# -*- coding: utf-8 -*-

from __future__ import division
import RPIO
import datetime
import math

RPIO.setwarnings(False)
RPIO.setup(8, RPIO.OUT)

res = []

def times(gpio_id, val):
	if len(res) < 6:
		res.append(int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 10000))
	else: 
		RPIO.stop_waiting_for_interrupts()

# GPIO interrupt callbacks
RPIO.add_interrupt_callback(7, times, edge="rising")

# Blocking main epoll loop
RPIO.wait_for_interrupts()

diff_list = []

for i in range(3):
	diff_list.append(res[i + 1] - res[i])	

diff = reduce(lambda x, y: x + y, diff_list) / len(diff_list)

tl = diff * 0.33

number = (tl / 10000) / 693

prefixes = {
	"mF" : 10**3, 
	"uF" : 10**6, 
	"nF" :10**9
}

for key, value in prefixes.iteritems():
	if number * value > 1 and number * value < 1000:
		print("Hodnota je {} {}".format(int(number * value), key))