'''PARALLEL, NOT USING INITIALIZATION'''
from matplotlib import pyplot
import numpy
import time
from multiprocessing import Pool, Array
import multiprocessing
import sys
start = time.time()

# initial conditions
size = 1000
num_processors = 2

y = multiprocessing.Array('d', 1000, lock=False)
y[480:520] = [1] * 40

#break up data, start-end
start_end = []
chunk_size = size//num_processors
for i in range(num_processors):
    start_end.append([i*chunk_size,chunk_size*(i+1)])

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
    new_y = list(y)
    for j in range(start,end):
        # diffusion via forward Euler
        new_y[j] += dt * (D * (y[j - 1] - 2 * y[j] + y[(j + 1) % size]))

        # reaction via forward Euler
        new_y[j] += dt * -y[j] * (1 - y[j]) * (alpha - y[j])

    return new_y[start:end]


pool = multiprocessing.Pool(processes=num_processors) #instantiate pool
# advance through t is at least 100; plot every 20
for t in numpy.arange(0, 100 + dt, dt):
    if t % 20 == 0:
        pyplot.plot(y, label='t = %g' % t)
    result = pool.map(advance, start_end)
    y[:] = [item for sublist in result for item in sublist]

print('calculation: {} s'.format(time.time() - start))

pyplot.legend()
pyplot.show()
