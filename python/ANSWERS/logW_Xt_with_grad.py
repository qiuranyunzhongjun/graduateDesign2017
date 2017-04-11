from numpy import *
from logMixtureDist import logMixtureDist

def logW_Xt_with_grad(vecW):
    global X, t, distFun, distPara_array, pi_array, muW1, muW2, lamW1, lamW2
    [xDim, serialLength] = shape(X)
    tDim = size(t, 0)
    W = reshape(vecW, [tDim, xDim])
    logWeibullMix = ones(shape(X))
    logWeibullMix_grad = ones(shape(X))
    prediction = W.T * t
    negativePredictionInd = where(prediction < 2)
    prediction[negativePredictionInd] = exp(prediction[negativePredictionInd] - 1 - 1) + 1
    for i in range(size(distPara_array,1)):
        ind = round(X) == i#不知道这里是不是i+1
        [logWeibullMix[ind], logWeibullMix_grad[ind]] = logMixtureDist(prediction[ind].T, distFun, reshape(distPara_array[:,i-1,i],2,-1,order='F'), pi_array[:,i-1,i])
    logW = -(sum(logWeibullMix)-0.5 * (W[0]*lamW1 * W[0].T)+(W[0]*lamW1*muW1)-0.5*(W[1]*lamW2*W[1].T)+(W[1]*lamW2 * muW2))
    T = tile(t[0], [xDim, 1])
    pred_gradW1 = T
    pred_gradW1[negativePredictionInd] = pred_gradW1[negativePredictionInd] * (prediction[negativePredictionInd] - 1)
    T = tile(t[1], [xDim, 1])
    pred_gradW2 = T
    pred_gradW2[negativePredictionInd] = pred_gradW2[negativePredictionInd] * (prediction[negativePredictionInd] - 1)
    grad1_1 = sum(logWeibullMix_grad * pred_gradW1, 1).reshape(-1,1) - lamW1 * W[0].T + lamW1 * muW1
    grad1_2 = sum(logWeibullMix_grad * pred_gradW2, 1).reshape(-1,1) - lamW2 * W[1].T + lamW2 * muW2
    gradW = array([grad1_1.T, grad1_2.T])
    gradW = -gradW[:].T
    return logW,gradW