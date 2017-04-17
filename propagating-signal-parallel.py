from matplotlib import pyplot
import time
import multiprocessing

#initialize some multiprocessing stuff
num_processes = 1
y = multiprocessing.Array('d', 1000, lock=False)
new_y = multiprocessing.Array('d', 1000, lock=True)
dt = multiprocessing.Value('d',0, lock=False)
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
[e for e in set(y)]
[e for e in set(new_y)]
# time-step
dt.value = 0.01

# our rule for reaction-diffusion
def advance(y_idx):
    #print y_idx
    new_y[y_idx] += dt.value * (20 * (y[y_idx - 1] - 2 * y[y_idx] + y[(y_idx + 1) % len(y)])
						   - y[y_idx] * (1 - y[y_idx]) * (0.3 - y[y_idx]))
    #Strange it seems to only update 2... i have no idea why investigating
    print (dt.value * (20 * (y[y_idx - 1] - 2 * y[y_idx] + y[(y_idx + 1) % len(y)])
						   - y[y_idx] * (1 - y[y_idx]) * (0.3 - y[y_idx])))
    #print new_y[y_idx]
    #return y_idx

# advance through t (t = i * dt) is at least 100; plot
# every 20
i = 0
p = multiprocessing.Pool(num_processes)
while i * dt.value <= 100:
    if i * dt.value % 20 == 0:
        pyplot.plot(y, label='t = %g' % (i * dt.value))
    p.map(advance, range(len(y)))
    #p.close()
    #p.join()
    y = new_y
    i += 1
    #print i * dt.value
end = time.time()

elapsed = end-start
print elapsed
pyplot.legend()
pyplot.show()