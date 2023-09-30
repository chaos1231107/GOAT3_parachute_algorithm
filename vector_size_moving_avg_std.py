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

#calculate vector size based on relative position
def cal_relative_vector(prev_position, curr_position):
    relative_vector_square = (curr_position - prev_position) ** 2
    vector_size = np.sqrt(sum(relative_vector_square))
    return vector_size

def moving_average(data, window):
    moving_avg = []
    for x in  range(len(data)):
        if x < window - 1:
            moving_avg.append(data[x])
        else:
            partial_avg = np.mean(data[x-window+1 : x+1])
            moving_avg.append(partial_avg)
    return moving_avg

data = []
window = 3
relative_vector = []
for j in range(1, TMS_data.shape[0]):
    prev_position = pos[j-1]
    curr_position = pos[j]
    result = cal_relative_vector(prev_position, curr_position)
    time.sleep(0.1)
    relative_vector.append(result)
    data.append(result)
    ma = moving_average(data, window)  # moving average
    print(relative_vector)
    if j >= window and ma[j - window] > ma[j - window + 1]:
        # 이전 이동평균이 이후 이동평균의 수치보다 클때 값을 더이상 받지 않는다
        break
    

time_stamp = range(1, len(relative_vector) + 1)

# Plot the differences in vector sizes
plt.plot(time_stamp, relative_vector, marker='o', linestyle='-')
plt.xlabel('Time Stamp')
plt.ylabel('Difference in Vector Size')
plt.title('Difference in Vector Size Over Time')
plt.grid(True)
plt.show()