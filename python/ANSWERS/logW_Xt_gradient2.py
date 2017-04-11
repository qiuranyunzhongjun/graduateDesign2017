from numpy import *
from logMixtureDist import logMixtureDist

def logW_Xt_gradient2(vecW):
    global X, t, distFun, distPara_array, pi_array, muW1, muW2, lamW1, lamW2
    [xDim, serialLength] = shape(X)
    tDim = size(t, 0)
    W = vecW.reshape(tDim, xDim,order='F')
    logWeibullMix = ones(shape(X))
    logWeibullMix_grad = ones(shape(X))
    logWeibullMix_grad2 = ones(shape(X))
    prediction = W.T*t
    negativePredictionInd = where(prediction < 2)
    prediction[negativePredictionInd] = exp(prediction[negativePredictionInd] - 1 - 1) + 1
    for i in range(size(distPara_array,1)):
        ind = round(X) == i#这个不知道是不是i
        [logWeibullMix[ind], logWeibullMix_grad[ind], logWeibullMix_grad2[ind]] = logMixtureDist(prediction[ind].T,
            distFun, reshape(distPara_array[:,i-1,i],2,-1,order='F'), pi_array[:,i-1,i])
    T1 = tile(t[0], (xDim, 1))
    T2 = tile(t[1], (xDim, 1))
    pred_gradW1 = T1
    pred_gradW1[negativePredictionInd] = T1[negativePredictionInd] * (prediction[negativePredictionInd] - 1)
    pred_gradWW1 = zeros(shape(X))
    pred_gradWW1[negativePredictionInd] = (prediction[negativePredictionInd] - 1) * T1[negativePredictionInd]** 2
    pred_gradW1W2 = zeros(shape(X))
    pred_gradW1W2[negativePredictionInd] = (prediction[negativePredictionInd] - 1) * T1[negativePredictionInd] * T2[negativePredictionInd]
    pred_gradW2 = T2
    pred_gradW2[negativePredictionInd] = T2[negativePredictionInd] * (prediction[negativePredictionInd] - 1)
    pred_gradWW2 = zeros(shape(X))
    pred_gradWW2[negativePredictionInd] = (prediction[negativePredictionInd] - 1) * T2[negativePredictionInd] ** 2
    grad2_1 = logWeibullMix_grad2 * pred_gradW1 ** 2 + logWeibullMix_grad * pred_gradWW1
    grad2_1 = diag(sum(grad2_1, 1).reshape(-1, 1)) - lamW1
    grad2_12 = logWeibullMix_grad2 * pred_gradW1 * pred_gradW2 + logWeibullMix_grad * pred_gradW1W2
    grad2_12 = diag(sum(grad2_12, 1).reshape(-1,1))
    grad2_2 = logWeibullMix_grad2 * pred_gradW2 ** 2 + logWeibullMix_grad * pred_gradWW2
    grad2_2 = diag(sum(grad2_2, 1).reshape(-1,1)) - lamW2
    gradW2 = zeros(3, xDim, xDim)
    gradW2[0] = grad2_1
    gradW2[1] = grad2_2
    gradW2[2]  = grad2_12
    return gradW2