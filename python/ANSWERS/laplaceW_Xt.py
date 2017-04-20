from numpy import *
from scipy.optimize import fmin, minimize
from logW_Xt_with_grad import logW_Xt_with_grad
from logW_Xt_gradient2 import logW_Xt_gradient2
import globalV
import csv

def dist2(X,Y):
    distMat = nan * ones((X.shape[0], Y.shape[0]))
    for i in range(X.shape[0]):
        for j in range(Y.shape[0]):
            distMat[i][j] = sum((X[i] - Y[j]) ** 2)
    return distMat


def laplaceW_Xt (X_in,t_in,distFun_in, distPara_array_in,pi_array_in, withSpatial=1,slopePrior=array(())):
    #global X,t, distFun, distPara_array, pi_array, muW1, muW2, lamW1, lamW2
    globalV.X = X_in.round()
    globalV.t = vstack((t_in,ones([1,len(t_in)])))
    globalV.distFun = distFun_in
    globalV.distPara_array = distPara_array_in
    globalV.pi_array = pi_array_in
    loc = array([ [ -9, 21 ], [ -3, 21 ],
        [ 3, 21 ], [ 9, 21 ], [ -15, 15 ], [ -9, 15 ], [ -3, 15 ],
        [ 3, 15 ], [ 9, 15 ], [ 15, 15 ], [ -21, 9 ], [ -15, 9 ],
        [ -9, 9 ], [ -3, 9 ], [ 3, 9 ], [ 9, 9 ], [ 15, 9 ], [ 21, 9 ],
        [ -27, 3 ], [ -21, 3 ], [ -15, 3 ], [ -9, 3 ], [ -3, 3 ], [ 3, 3 ],
        [ 9, 3 ], [ 15, 3 ], [ 21, 3 ], [ -27, -3 ], [ -21, -3 ],
        [ -15, -3 ], [ -9, -3 ], [ -3, -3 ], [ 3, -3 ], [ 9, -3 ],
        [ 15, -3 ], [ 21, -3 ], [ -21, -9 ], [ -15, -9 ], [ -9, -9 ],
        [ -3, -9 ], [ 3, -9 ], [ 9, -9 ], [ 15, -9 ], [ 21, -9 ],
        [ -15, -15 ], [ -9, -15 ], [ -3, -15 ], [ 3, -15 ], [ 9, -15 ],
        [ 15, -15 ], [ -9, -21 ], [ -3, -21 ], [ 3, -21 ], [ 9, -21 ] ])
    SFR = pi - array([268,262,252,245,264,274,281,275,260,246,271,285,291,296,298,283,253,229,278,287,291,298,312,329,318,1,
                      218,83,76,68,55,34,11,13,1,167,85,78,66,56,48,60,95,136,88,81,77,80,93,112,93,95,100,108]) * pi / 180.0
    loc = delete(loc, 25, axis=0)
    loc = delete(loc, 33, axis=0)
    SFR = delete(SFR, 25)
    SFR = delete(SFR, 33)
    distMat = dist2(loc, loc)
    angDisMat = sqrt(dist2(SFR.T, SFR.T))
    angDisMat[angDisMat > pi] = 2 * pi - angDisMat[angDisMat > pi]
    angDisMat = angDisMat**2
    if slopePrior.size == 0:
        globalV.muW1 = zeros([size(globalV.X, 0),1])
        A1 = 10
    else:
        globalV.muW1 = slopePrior(1) * ones([size(globalV.X, 0),1])
        A1 = slopePrior[1]
    globalV.muW2 = median(globalV.X, 1)
    A2 = 10
    L = 6
    angL = 15 * pi / 180
    distMat1 = A1 ** 2 * exp(-0.5 * (0.5 * distMat / L ** 2 + 0.5 * angDisMat / angL ** 2))
    distMat2 = A2 ** 2 * exp(-0.5*(0.5 * distMat / L ** 2 + 0.5 * angDisMat / angL ** 2))
    if not withSpatial:
        distMat1 = diag(diag(distMat1))
        distMat2 = diag(diag(distMat2))
    distMat1[0: 26, 26: 52] = 0
    distMat1[26: 52, 0: 26] = 0
    distMat2[0: 26, 26: 52] = 0
    distMat2[26: 52, 0: 26] = 0
    globalV.lamW1 = linalg.inv(distMat1)
    globalV.lamW2 = linalg.inv(distMat2)

    '''
    options = foptions;
    options(1) = 0;
    options(9) = 0;
    options(14) = 300;
    '''

    oldW = vstack((zeros([1, 52]),median(globalV.X,1)))

    '''
    options = optimoptions('fminunc','GradObj','on','Algorithm','trust-region','DerivativeCheck', 'off', 'Diagnostics', 'off', 'Display', 'off', 'MaxIter', 400);
    %找到最小的无约束多变量函数的非线性编程求解器，GradObj:用户定义的目标函数的梯度，将算法设置为'trust-region',Diagnostics: 打印最小化函数的诊断信息,
    derivativeCheck:对用户提供的导数和有限差分求出的导数进行对比,Display:显示水平,选择'off'，不显示输出,MaxIter:最大允许迭代次数 400；
    [newW] = fminunc('logW_Xt_with_grad',oldW(:)',options);
    '''
    oldW_T = vstack(split(oldW,size(oldW,1),axis=1)).T
    newW = fmin(logW_Xt_with_grad, oldW_T , xtol=1e-8, maxiter=400, disp=0)

    '''
    csv_reader = csv.reader(open('tempdata\\standNewW.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    newW = array(tempList)
    '''
    newW = newW.reshape(2, -1,order='F')
    gradW2 = logW_Xt_gradient2(vstack(split(newW,size(newW,1),axis=1)))
    return newW, gradW2
if __name__ == "__main__":
    globalV.distFun = 'weibull'
    csv_reader = csv.reader(open('tempdata\\X.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    globalV.X = array(tempList)
    csv_reader = csv.reader(open('tempdata\\t.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    globalV.t = array(tempList)
    csv_reader = csv.reader(open('tempdata\\distPara_array.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    globalV.distPara_array = array(tempList)
    csv_reader = csv.reader(open('tempdata\\pi_array.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    globalV.pi_array = array(tempList)
    csv_reader = csv.reader(open('tempdata\\muW1.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    globalV.muW1 = array(tempList)
    csv_reader = csv.reader(open('tempdata\\muW2.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    globalV.muW2 = array(tempList)
    csv_reader = csv.reader(open('tempdata\\lamW1.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    globalV.lamW1 = array(tempList)
    csv_reader = csv.reader(open('tempdata\\lamW2.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    globalV.lamW2 = array(tempList)
    csv_reader = csv.reader(open('tempdata\\oldW_T.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    oldW_T = array(tempList)
    csv_reader = csv.reader(open('tempdata\\standNewW.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    standNewW = array(tempList)
    newW = fmin(logW_Xt_with_grad, oldW_T, xtol=1e-8, maxiter=400, disp=0)
    newW1 = minimize(logW_Xt_with_grad, oldW_T, method='trust-ncg',
                     options = {'xtol': 1e-8, 'maxiter':400, 'disp': False})
    print('newW')
    print(newW)
    print('standNewW')
    print(standNewW)
    print('newW1')
    print(newW1)
