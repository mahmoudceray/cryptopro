
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
التطبيق الأول:  القسم الثاني, التوقع باستخدام متغير واحد
---------------------------------------------------------------

●	رابط الفيديو
https: // youtu.be/SsNjJ6av27I


●	البيانات
6.1101, 17.592
5.5277, 9.1302
8.5186, 13.662
7.0032, 11.854
5.8598, 6.8233
8.3829, 11.886
7.4764, 4.3483
8.5781, 12
6.4862, 6.5987
5.0546, 3.8166
5.7107, 3.2522
14.164, 15.505
5.734, 3.1551
8.4084, 7.2258
5.6407, 0.71618
5.3794, 3.5129
6.3654, 5.3048
5.1301, 0.56077
6.4296, 3.6518
7.0708, 5.3893
6.1891, 3.1386
20.27, 21.767
5.4901, 4.263
6.3261, 5.1875
5.5649, 3.0825
18.945, 22.638
12.828, 13.501
10.957, 7.0467
13.176, 14.692
22.203, 24.147
5.2524, -1.22
6.5894, 5.9966
9.2482, 12.134
5.8918, 1.8495
8.2111, 6.5426
7.9334, 4.5623
8.0959, 4.1164
5.6063, 3.3928
12.836, 10.117
6.3534, 5.4974
5.4069, 0.55657
6.8825, 3.9115
11.708, 5.3854
5.7737, 2.4406
7.8247, 6.7318
7.0931, 1.0463
5.0702, 5.1337
5.8014, 1.844
11.7, 8.0043
5.5416, 1.0179
7.5402, 6.7504
5.3077, 1.8396
7.4239, 4.2885
7.6031, 4.9981
6.3328, 1.4233
6.3589, -1.4211
6.2742, 2.4756
5.6397, 4.6042
9.3102, 3.9624
9.4536, 5.4141
8.8254, 5.1694
5.1793, -0.74279
21.279, 17.929
14.908, 12.054
18.959, 17.054
7.2182, 4.8852
8.2951, 5.7442
10.236, 7.7754
5.4994, 1.0173
20.341, 20.992
10.136, 6.6799
7.3345, 4.0259
6.0062, 1.2784
7.2259, 3.3411
5.0269, -2.6807
6.5479, 0.29678
7.5386, 3.8845
5.0365, 5.7014
10.274, 6.7526
5.1077, 2.0576
5.7292, 0.47953
5.1884, 0.20421
6.3557, 0.67861
9.7687, 7.5435
6.5159, 5.3436
8.5172, 4.2415
9.1802, 6.7981
6.002, 0.92695
5.5204, 0.152
5.0594, 2.8214
5.7077, 1.8451
7.6366, 4.2959
5.8707, 7.2029
5.3054, 1.9869
8.2934, 0.14454
13.394, 9.0551
5.4369, 0.61705


●	الكود
#import libraries

# read data
path = 'D:\\z\\1\\ex1data1.txt'
data = pd.read_csv(path, header=None, names=['Population', 'Profit'])

# show data details
print('data = \n', data.head(10))
print('**************************************')
print('data.describe = \n', data.describe())
print('**************************************')
# draw data
data.plot(kind='scatter', x='Population', y='Profit', figsize=(5, 5))

# =========================================================================

# adding a new column called ones before the data
data.insert(0, 'Ones', 1)
print('new data = \n', data.head(10))
print('**************************************')


# separate X (training data) from y (target variable)
cols = data.shape[1]
X = data.iloc[:, 0:cols-1]
y = data.iloc[:, cols-1:cols]

print('**************************************')
print('X data = \n', X.head(10))
print('y data = \n', y.head(10))
print('**************************************')


# convert from data frames to numpy matrices
X = np.matrix(X.values)
y = np.matrix(y.values)
theta = np.matrix(np.array([0, 0]))

print('X \n', X)
print('X.shape = ', X.shape)
print('theta \n', theta)
print('theta.shape = ', theta.shape)
print('y \n', y)
print('y.shape = ', y.shape)
print('**************************************')

# =========================================================================
# cost function


def computeCost(X, y, theta):
    z = np.power(((X * theta.T) - y), 2)
#    print('z \n',z)
#    print('m ' ,len(X))
    return np.sum(z) / (2 * len(X))


print('computeCost(X, y, theta) = ', computeCost(X, y, theta))

print('**************************************')


# GD function
def gradientDescent(X, y, theta, alpha, iters):
    temp = np.matrix(np.zeros(theta.shape))
    parameters = int(theta.ravel().shape[1])
    cost = np.zeros(iters)

    for i in range(iters):
        error = (X * theta.T) - y

        for j in range(parameters):
            term = np.multiply(error, X[:, j])
            temp[0, j] = theta[0, j] - ((alpha / len(X)) * np.sum(term))

        theta = temp
        cost[i] = computeCost(X, y, theta)

    return theta, cost


# initialize variables for learning rate and iterations
alpha = 0.01
iters = 1000

# perform gradient descent to "fit" the model parameters
g, cost = gradientDescent(X, y, theta, alpha, iters)

print('g = ', g)
print('cost  = ', cost[0:50])
print('computeCost = ', computeCost(X, y, g))
print('**************************************')


# =========================================================================

# get best fit line

x = np.linspace(data.Population.min(), data.Population.max(), 100)
print('x \n', x)
print('g \n', g)

f = g[0, 0] + (g[0, 1] * x)
print('f \n', f)


# draw the line

fig, ax = plt.subplots(figsize=(5, 5))
ax.plot(x, f, 'r', label='Prediction')
ax.scatter(data.Population, data.Profit, label='Traning Data')
ax.legend(loc=2)
ax.set_xlabel('Population')
ax.set_ylabel('Profit')
ax.set_title('Predicted Profit vs. Population Size')


# draw error graph

fig, ax = plt.subplots(figsize=(5, 5))
ax.plot(np.arange(iters), cost, 'r')
ax.set_xlabel('Iterations')
ax.set_ylabel('Cost')
ax.set_title('Error vs. Training Epoch')
