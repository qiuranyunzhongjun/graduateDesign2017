import csv
from numpy import *
from logW_Xt_with_grad import logW_Xt_with_grad
from scipy.optimize import fmin

'''
csv_reader = csv.reader(open('oldW.csv', encoding='utf-8'))
oldW_L = []
for row in csv_reader:
    oldW_L.append(list(map(float, row)))
oldW = array(oldW_L)
csv_reader = csv.reader(open('standNewW.csv', encoding='utf-8'))
standNewW_L = []
for row in csv_reader:
    standNewW_L.append(list(map(float, row)))
standNewW = array(standNewW_L)
oldW_T = vstack(split(oldW,size(oldW,1),axis=1)).T
[newW] = fmin(logW_Xt_with_grad, oldW_T , maxiter=400, disp=0)
if newW == standNewW:
    print('pass')
'''
def rosen(x):
    f = 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2;
    g = vstack((-400 * (x[1] - x[0] ** 2) * x[0] - 2 * (1 - x[0]),200 * (x[1] - x[0] ** 2)))
    #r = sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)
    return f,g

if __name__ == "__main__":
    print('start')
    x0 = [-1 , 2]
    xopt = fmin(rosen, x0, xtol=1e-8)
    print(xopt)
