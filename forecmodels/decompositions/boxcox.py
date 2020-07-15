import numpy as np


class boxcox:

    def __init__(self):
        pass

    def x_transform(x, lambd1):
        if lambd1 == 0:
            return np.log(x)
        else:
            return (x**lambd1 - 1)/lambd1


    def log_equation(Data, lambd):
        T = len(data)
        mean = np.array([boxcox.x_transform(a, lambd)
                         for a in data.values[:, 1]]).mean()
        log_L = -T/2*np.log(sum((boxcox.x_transform(i, lambd)-mean)**2
                                for i in data.values[:, 1])/T)+(lambd-1)*sum(np.log(i)for i in data.values[:, 1])
        return log_L


    def transform(data):
        L = lambda args: -boxcox.log_equation(data, args[0])

        x0 = [1]
        bounds = [-1, 1]
        res = minimize(L,  bounds=bounds, method = 'dihotomy').fit()

        return [boxcox.x_transform(data, res[0]), res[0]]


    def reverse(data, param):
        if param != 0:
            return np.exp(np.log(param*data + 1) / param)
        else:
            return np.exp(data)
