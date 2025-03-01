import numpy as np


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=1, keepdims=True)


def logloss(Y, Y_hat) -> float:
    # Y and Y_hat have both rank n x m, where n is the number of examples and m number of classes
    eps = 1e-15
    return -np.mean(np.sum(Y * np.log(softmax(Y_hat) + eps), axis=1))


X = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
Y = np.array([[3.0, 2.0, 2.0], [2.0, 5.0, 3.0]])

print(softmax(Y))
print(logloss(X, Y))
