from matplotlib import pyplot
import time
import multiprocessing

#initialize some multiprocessing stuff
num_processes = 4
y = multiprocessing.Array('d', 1000, lock=False)
new_y = multiprocessing.Array('d', 1000, lock=False)
dt = multiprocessing.Value('d',0, lock=False)
y_len = multiprocessing.Value('i',len(y), lock=False)
#def init_process(y_to_share, new_y_to_share):
#	global y, new_y
#	y = y_to_share
#	new_y = new_y_to_share
#
#process_pool = multiprocessing.Pool(
#                   num_processes,
#                   initializer=init_process,
#                   initargs=(y, new_y))


start = time.time()
# initial conditions
#y = [0] * 1000
y[480:520] = [1] * 40
#check y values
#[e for e in set(y)]
#[e for e in set(new_y)]
#[e for e in set(arr)]
# time-step
dt.value = 0.01

# our rule for reaction-diffusion
def advance(j):
    #print y_idx
    #new_y[j]
    result = (y[j] + dt.value * (20 * (y[j - 1] - 2 * y[j] + y[(j + 1) % y_len.value])
						   - y[j] * (1 - y[j]) * (0.3 - y[j])))
    y[j] = result
    return result

# advance through t (t = i * dt) is at least 100; plot
# every 20
i = 0
p = multiprocessing.Pool(num_processes)
y_range = range(len(y))
while i * dt.value <= 100:
    if i * dt.value % 20 == 0:
        pyplot.plot(y, label='t = %g' % (i * dt.value))
    arr = p.map(advance, y_range)
    #p.close()
    #p.join()
#    for idx in range(len(arr)):
#        y[idx] = arr[idx]
    i += 1
    print i * dt.value
end = time.time()

elapsed = end-start
print elapsed
pyplot.legend()
pyplot.show()

ny = list(y)