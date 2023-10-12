import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

#Read file
TMS_data = pd.read_json('data.json')
targets = TMS_data['target']
pos = []
for target in targets:
    position = target['position']
    pos.append([position['x'], position['y'], position['z']])
pos = np.array(pos)

#Calculate vector size based on relative position
def cal_relative_vector(curr_position, prev_position):
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

for j in range(1, TMS_data.shape[0]):
    prev_position = pos[j-1]
    curr_position = pos[j]
    result = cal_relative_vector(prev_position, curr_position)
    relative_vector.append(result)
    data.append(result)
    print(result)
    time.sleep(0.1)
    time_stamp.append(j)

    ma = moving_average(data, window)
    ma = np.array(ma)
    # estimatedRTT[n] = (1-alpha) * Estimated[n-1] + alpha * sampleRTT[n]
    estimated = ma[-1]
    estimated = (1-alpha) * estimated + alpha * result
    #DevRTT[n] = (1-beta) * DevRTT[n-1] + beta * |SampleRTT - Estimated|
    var = np.var(data[-window:]) # read last three data for size of window(window=3)
    var = (1-beta)*var + beta * (abs(result - estimated))
    moving_std.append(np.sqrt(var))


#Plot values
plt.plot(time_stamp, relative_vector,label='Difference in Vector Size')
plt.plot(time_stamp, ma, label='Moving Average', color='red')
plt.plot(time_stamp, np.array(ma) + np.array(moving_std), label='Moving Aeverage + 1sigma')
plt.plot(time_stamp, np.array(ma) - np.array(moving_std), label='Moving Average - 1sigma')
plt.legend()
plt.show()