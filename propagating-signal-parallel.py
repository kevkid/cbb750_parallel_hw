#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 22:02:54 2017

@author: kevin
"""

from matplotlib import pyplot
import time
from multiprocessing import Pool, Array
import multiprocessing
from functools import partial
from contextlib import closing
start = time.time()
# initial conditions
y = [0] * 1000
y[480:520] = [1] * 40

# time-step
dt = 0.01

# our rule for reaction-diffusion
def advance(dt, y):
	#global y
	n = len(y)
	new_y = list(y)
	for j in xrange(n):#these communicate with the previous one and the one after
		new_y[j] += dt * (20 * (y[j - 1] - 2 * y[j] + y[(j + 1) % n])
						   - y[j] * (1 - y[j]) * (0.3 - y[j]))#this part can be parallalized
	y = new_y#we can just do each new_y on its own process
    print new_y
    return new_y

# advance through t (t = i * dt) is at least 100; plot
# every 20
#number of processors
num_processors = 2
y = multiprocessing.Array('d', 1000, lock=False)
i = 0
while i * dt <= 100:
	if i * dt % 20 == 0:
		pyplot.plot(y, label='t = %g' % (i * dt))
    with closing(Pool(processes=num_processors)) as p:
        newys = chunkIt(y, num_processors)
        func = partial(advance, dt)
        ny = p.map(func, newys)
        p.close()
        p.join()
	i += 1
	print i * dt
end = time.time()

elapsed = end-start
print elapsed
pyplot.legend()
pyplot.show()

def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0

  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out
