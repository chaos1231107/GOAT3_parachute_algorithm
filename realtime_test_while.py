import numpy as np
import time
import matplotlib.pyplot as plt
import random

# Calculate vector size based on relative position
def cal_relative_vector(prev_position, curr_position):
    vector_size = np.linalg.norm(prev_position - curr_position)  # calculate 'Three Dimensional Euclidean Distance'
    return vector_size

def moving_average(data, window):
    moving_avg = []
    for i in range(len(data)):
        if i < window - 1:
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

while True:
    # Generate random real number (0 ~ 100)
    curr_position = np.array([random.uniform(0, 100), random.uniform(0, 100), random.uniform(0, 100)])
    
    if data: # if list is not empty --> True  
        prev_position = data[-1]  
    else:
        prev_position = curr_position  
    
    result = cal_relative_vector(prev_position, curr_position)
    relative_vector.append(result)
    data.append(curr_position)  # Append the current position to the list
    time_stamp.append(len(data))

    ma = moving_average(relative_vector, window)
    ma = np.array(ma)
    estimated = ma[-1]
    
    estimated = (1 - alpha) * estimated + alpha * result
    var = np.var(relative_vector[-window:])
    var = (1 - beta) * var + beta * (abs(result - estimated))
    moving_std.append(np.sqrt(var))

    # Plot values
    plt.clf()
    plt.plot(time_stamp, relative_vector, label='Difference in Vector Size')
    plt.plot(time_stamp, ma, label='Moving Average', color='red')
    plt.plot(time_stamp, np.array(ma) + np.array(moving_std), label='Moving Average + 1sigma')
    plt.plot(time_stamp, np.array(ma) - np.array(moving_std), label='Moving Average - 1sigma')
    plt.grid(True)
    plt.legend()
    plt.pause(0.1)
