import numpy as np
import pandas as pd
import time
import bottleneck as bn

data = pd.read_json('data.json')

targets = data['target']
pos = []
for target in targets:
    position = target['position']
    pos.append([position['x'], position['y'], position['z']])

pos = np.array(pos)

#calculate size of vetor
def cal_vector_size(x, y, z):
    previous_position = np.array([pos[0]])
    current_position = np.array([x, y, z])
    square_distance = (current_position - previous_position) ** 2
    previous_position[:] = current_position
    vector_size = np.sqrt(np.sum(square_distance))
    return vector_size

#calculate moving average
def moving_average(data, window):
    moving_average = []
    for i in range(len(data)):
        if i < window-1:
            moving_average.append(data[i])
        else:
            partial_avg = np.mean(data[i-window+1 : i+1])
            moving_average.append(partial_avg)
    return moving_average

x_position = pos[:, 0]
y_position = pos[:, 1]
z_position = pos[:, 2]
data2 = []
# result = []
for j in range(1, data.shape[0]):
    result_prev = cal_vector_size(x_position[j-1], y_position[j-1], z_position[j-1])
    result_last = cal_vector_size(x_position[j], y_position[j], z_position[j])

    window = 4
    constraint = 15
    data2.append(result_last)
    moving_avg = moving_average(data2, window)
    print(f'moving average = {moving_avg[-1]}')

    #check error of sensor
    if abs(result_last - moving_avg[-1]) > constraint:
        print('error')


    print(f'vector_size = {result_last}')
    time.sleep(0.1)

    if result_prev > result_last:
        break
