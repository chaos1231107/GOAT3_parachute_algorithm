import numpy as np
import pandas as pd
import time

data = pd.read_json('data.json')

targets = data['target']
pos = []
for target in targets:
    position = target['position']
    pos.append([position['x'], position['y'], position['z']])

pos = np.array(pos)

#벡터크기 구하는 함수
def cal_vector_size(x, y, z):
    previous_position = np.array([pos[0]])
    current_position = np.array([x, y, z])
    square_distance = (current_position - previous_position) ** 2
    previous_position[:] = current_position
    vector_size = np.sqrt(np.sum(square_distance))
    return vector_size

x_position = pos[:, 0]
y_position = pos[:, 1]
z_position = pos[:, 2]

for i in range(1, data.shape[0]):
    result_prev = cal_vector_size(x_position[i-1], y_position[i-1], z_position[i-1])
    result_last = cal_vector_size(x_position[i], y_position[i], z_position[i])

    #계산된 벡터가 에러인지 체크하는 코드 추가


    print(f'vector_size = {result_last}')
    time.sleep(0.1)

    if result_prev > result_last:
        break
