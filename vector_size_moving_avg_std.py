import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

# Read file 
TMS_data = pd.read_json('data.json')
targets = TMS_data['target']
pos = []
for target in targets:
    position = target['position']
    pos.append([position['x'], position['y'], position['z']])
pos = np.array(pos)

# Calculate vector size based on relative position
def cal_relative_vector(prev_position, curr_position):
    relative_vector_square = (curr_position - prev_position) ** 2
    vector_size = np.sqrt(sum(relative_vector_square))
    return vector_size

# Calculate moving average
def moving_average(data, window):
    moving_avg = []
    for i in range(len(data)):
        if i < window - 1:
            moving_avg.append(data[i])
        else:
            partial_avg = np.mean(data[i - window + 1 : i + 1])
            moving_avg.append(partial_avg)
    return moving_avg

data = []
window = 3
relative_vector = []
time_stamp = []
error_point = []
error_cnt = 0

for j in range(1, TMS_data.shape[0]):
    prev_position = pos[j - 1]
    curr_position = pos[j]
    result = cal_relative_vector(prev_position, curr_position)
    relative_vector.append(result)
    data.append(result)
    ma = moving_average(data, window)  # Moving average
    time_stamp.append(j)
    print(relative_vector)
    time.sleep(0.1)
    
    # Calculate moving variance for the last 'window' values
    if len(data) >= window:
        moving_var = np.var(data[-window:]) #choose last three(window=3) values of data(list)
        if abs(result - ma[-1]) >  np.sqrt(moving_var):
            result = ma[-1]
    # if previous moving average > current moving average, break
    if j >= window and ma[j - window] > ma[j - window + 1]:
        break

#Plot the differences in vector sizes and moving average
plt.plot(time_stamp, relative_vector, marker='o', linestyle='-', label='Difference in Vector Size')
#Plot moving average history, slicing the list(ma) value to extract the last len(time_stamp) elements 
plt.plot(time_stamp, ma[-len(time_stamp):], marker='o', linestyle='-', color='red', label='Moving Average history')
plt.legend()
plt.xlabel('Time Stamp')
plt.ylabel('Value')
plt.title('Difference in Vector Size and Moving Average Over Time')
plt.legend()
plt.grid(True)
plt.show()

