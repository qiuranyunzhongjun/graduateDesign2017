from numpy import *
from logMixtureDist import logMixtureDist
import globalV
import csv

def logW_Xt_with_grad(vecW):
    #global X, t, distFun, distPara_array, pi_array, muW1, muW2, lamW1, lamW2
    [xDim, serialLength] = shape(globalV.X)
    tDim = size(globalV.t, 0)
    W = reshape(vecW, [tDim, xDim],order='F')
    logWeibullMix = ones(shape(globalV.X))
    logWeibullMix_grad = ones(shape(globalV.X))
    prediction = dot(W.T , globalV.t)
    negativePredictionInd = where(prediction < 2)
    prediction[negativePredictionInd] = exp(prediction[negativePredictionInd] - 1 - 1) + 1
    for i in range(size(globalV.distPara_array,1)):
        ind = globalV.X.round() == i+1#不知道这里是不是i
        [logWeibullMix.T[ind.T], logWeibullMix_grad.T[ind.T], songlijun] = logMixtureDist(prediction.T[ind.T], globalV.distFun, reshape(globalV.distPara_array[:,(i,)],[2,-1],order='F'), globalV.pi_array[:,(i,)])
    logW = -(sum(logWeibullMix)-0.5 * dot(dot(W[0],globalV.lamW1) , W[0].T)+dot(dot(W[0],globalV.lamW1),globalV.muW1)-0.5*dot(dot(W[1],globalV.lamW2),W[1].T)+dot(dot(W[1], globalV.lamW2) , globalV.muW2))
    T = tile(globalV.t[0], [xDim, 1])
    pred_gradW1 = T
    pred_gradW1[negativePredictionInd] = pred_gradW1[negativePredictionInd] * (prediction[negativePredictionInd] - 1)
    T = tile(globalV.t[1], [xDim, 1])
    pred_gradW2 = T
    pred_gradW2[negativePredictionInd] = pred_gradW2[negativePredictionInd] * (prediction[negativePredictionInd] - 1)
    grad1_1 = sum(logWeibullMix_grad * pred_gradW1, 1).reshape(-1,1) - dot(globalV.lamW1, W[0].T).reshape(-1,1) + dot(globalV.lamW1 , globalV.muW1)
    grad1_2 = sum(logWeibullMix_grad * pred_gradW2, 1).reshape(-1,1) - dot(globalV.lamW2 , W[1].T).reshape(-1,1) + dot(globalV.lamW2 , globalV.muW2)
    gradW = vstack((grad1_1.T, grad1_2.T))
    gradW = -vstack(split(gradW,size(gradW,1),axis=1)).T
    #return logW,gradW
    return logW

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
    csv_reader = csv.reader(open('tempdata\\oldW.csv', encoding='utf-8'))
    tempList = []
    for row in csv_reader:
        tempList.append(list(map(float, row)))
    oldW = array(tempList)
    oldW_T = vstack(split(oldW, size(oldW, 1), axis=1)).T
    logW_Xt_with_grad(oldW_T)