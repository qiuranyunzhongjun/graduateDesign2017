from numpy import *
from STRegression import STRegression
from scipy.stats import *

def STTrendAnalysis(X, t, distPara_array, pi_array, sigChangPerYear, p_val, withSpatial=1, slopePrior=array(())):
    adjustedX = X
    [slop, intercept, slopSD, interceptSD] = STRegression(adjustedX, t, distPara_array, pi_array, withSpatial,slopePrior)
    slopSD = abs(slopSD)
    pv = slop
    pv[slop > 0] = 1 - norm.cdf(0, slop[slop > 0], slopSD(slop > 0))
    pv[slop <= 0] = norm.cdf(0, -slop[slop <= 0], slopSD[slop <= 0])
    progressPt = (pv < p_val) & (slop < sigChangPerYear)
    progressPt[:]=1
    S = -log(pv) * progressPt
    S[progressPt == 0] = 0
    S = sum(S)
    return S, pv, slop, intercept, slopSD, interceptSD