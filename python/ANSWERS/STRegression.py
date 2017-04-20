from numpy import *
from laplaceW_Xt import laplaceW_Xt

def STRegression(X, t, distPara_array, pi_array, withSpatial=1, slopePrior=array(())):
    [w, gradW2] = laplaceW_Xt(X, t, 'weibull', distPara_array, pi_array, withSpatial, slopePrior)
    slop = w[0].T
    intercept = w[1].T
    SD = sqrt(-diag(linalg.inv(vstack((hstack((gradW2[0], gradW2[2])),hstack((gradW2[2], gradW2[1])))))))
    slopSD = SD[0:52]
    interceptSD = SD[52:104]
    return slop, intercept, slopSD, interceptSD