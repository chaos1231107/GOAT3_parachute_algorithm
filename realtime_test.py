import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import random

# make random numbers


# Calculate vector size based on relative position
def cal_relative_vector(prev_position, curr_position):
    vector_size = np.linalg.norm(prev_position - curr_position) #calculate 'Three Dimentional Eucliean Distance'
    return vector_size

def moving_average(data, window):
    moving_avg = []
    for i in range(len(data)):
        if i < window - i:
            moving_avg.append(data[i])
        else:
            partial_avg = np.mean(data[i - window + 1 : i + 1])
            moving_avg.append(partial_avg)
    return moving_avg

relative_vector = []
time_stamp = []
window = 3
data = []
moving_std = []
beta = 0.25
alpha = 0.125
radn_samples = 100

for j in range(radn_samples):
    # generate random real number 0 to 5
    prev_position = np.array([random.uniform(0,5), random.uniform(0,5), random.uniform(0,5)])
    curr_position = np.array([random.uniform(0,5), random.uniform(0,5), random.uniform(0,5)])
    result = cal_relative_vector(prev_position, curr_position)
    relative_vector.append(result)
    data.append(result)
    print(result)
    time.sleep(0.1)
    time_stamp.append(j)

    ma = moving_average(data, window)
    ma = np.array(ma)
    estimated = ma[-1]
    # moving_std.append(np.std(data[-window:]))
    estimated = (1-alpha) * estimated + alpha*result
    var = np.var(data[-window:])
    var = (1-beta)*var + beta*(abs(result - estimated))
    moving_std.append(np.sqrt(var))


#Plot values
plt.plot(time_stamp, relative_vector,label='Difference in Vector Size')
plt.plot(time_stamp, ma, label='Moving Average', color='red')
plt.plot(time_stamp, np.array(ma) + np.array(moving_std), label='Moving Aeverage + 1sigma')
plt.plot(time_stamp, np.array(ma) - np.array(moving_std), label='Moving Average - 1sigma')
plt.legend()
plt.show()