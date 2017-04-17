#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 19:57:10 2017

@author: kevin
"""
import multiprocessing

num_processes = 2
y = multiprocessing.Array('d', 6, lock=False)
for i in range(0,3):
    y[i] = 1
[e for e in y]

new_y = multiprocessing.Array('d', 6, lock=False)
idx = multiprocessing.Value('i',0, lock=True)
def init_process(y_to_share, new_y_to_share):
	global y, new_y
	y = y_to_share
	new_y = new_y_to_share

process_pool = multiprocessing.Pool(
                   num_processes,
                   initializer=init_process,
                   initargs=(y, new_y))

#y = [1,2,3,4,5,6]
dt = 0.0001
def sq(x):
     i = idx.value
     idx.value += 1
     print i
     v = y[i-1] + y[i] + y[(i + 1) % len(y)]
     #idx.value += 1
     return v
  #print multiprocessing.current_process()
  #print multiprocessing.Value
  #Here I want to do y at the current index and add the y value of the next index
  #something like new_y[i] = y[i]+y[i+1]

new_y = process_pool.map(sq, y)#spits out what y is
idx.value = 0
for i in range(0, len(new_y)):
    y[i] = new_y[i]
    
