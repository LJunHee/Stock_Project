import numpy as np
def transform_data(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        tmp = data[i:(i + time_step), 0]
        X.append(tmp)
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

# data에서 날짜 열을 제거하고 종가 열만 사용
data = np.array([
    [100],
    [105],
    [110],
    [115],
    [120]
])

X, y = transform_data(data, time_step=2)
print("X:", X)
print("y:", y)
