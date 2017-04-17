#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 21:55:16 2017

@author: kevin
"""

from matplotlib import pyplot
import time
start = time.time()
# initial conditions
y = [0] * 1000
y[480:520] = [1] * 40

# time-step
dt = 0.01

# our rule for reaction-diffusion
def advance(dt):
	global y
	n = len(y)
	new_y = list(y)
	for j in xrange(n):
		new_y[j] += dt * (20 * (y[j - 1] - 2 * y[j] + y[(j + 1) % n])
						   - y[j] * (1 - y[j]) * (0.3 - y[j]))
	y = new_y

# advance through t (t = i * dt) is at least 100; plot
# every 20
i = 0
while i * dt <= 100:
	if i * dt % 20 == 0:
		pyplot.plot(y, label='t = %g' % (i * dt))
	advance(dt)
	i += 1
	print i * dt
end = time.time()

elapsed = end-start
print elapsed
pyplot.legend()
pyplot.show()