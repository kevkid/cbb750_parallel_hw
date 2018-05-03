#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 13:15:07 2018

@author: kevin
"""

'''PARALLEL USING INITIALIZATION'''
from matplotlib import pyplot
import numpy
import time
import multiprocessing
import sys
start = time.time()

# initial conditions
size = 1000
num_processors = 2

y = multiprocessing.Array('d', 1000, lock=False)
new_y = multiprocessing.Array('d', 1000, lock=False)
y[480:520] = [1] * 40

#break up data, start-end
start_end = []
chunk_size = size//num_processors
for i in range(num_processors):
    start_end.append([i*chunk_size,chunk_size*(i+1)])

def init_process(y_to_share, new_y_to_share):
    global y, new_y
    y = y_to_share
    new_y = new_y_to_share

# parameters
D = 20         # diffusion constant/dx^2
alpha = 0.3    # threshold

# time-step
dt = 0.01

# our rule for reaction-diffusion
def advance(start_end):
    start = start_end[0]
    end = start_end[1]
    #print("hello, I am worker: {}".format(multiprocessing.current_process()))
    #print("start:{} end:{}".format(start,end))
    #sys.stdout.flush()
    #new_y[:] = y[:]
    for j in range(start,end):
        # diffusion via forward Euler
        new_y[j] += dt * (D * (y[j - 1] - 2 * y[j] + y[(j + 1) % size]))

        # reaction via forward Euler
        new_y[j] += dt * -y[j] * (1 - y[j]) * (alpha - y[j])



#initialize our processing pool
process_pool = multiprocessing.Pool(
                       processes=num_processors,
                       initializer=init_process,
                       initargs=(y, new_y))

#pool = multiprocessing.Pool(processes=num_processors) #instantiate pool
# advance through t is at least 100; plot every 20
new_y[:] = y[:]
for t in numpy.arange(0, 100 + dt, dt):
    if t % 20 == 0:
        pyplot.plot(y, label='t = %g' % t)
    process_pool.map(advance, start_end)
    y[:] = new_y[:]#[item for sublist in result for item in sublist]

print('calculation: {} s'.format(time.time() - start))

pyplot.legend()
pyplot.show()
