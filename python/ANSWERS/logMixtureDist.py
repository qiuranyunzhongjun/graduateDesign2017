from numpy import *

def logMixtureDist(x, distFun, distPara, pi_):
    [PDF, dPDF_dX, dPDF_dX2] = distFun(x, distPara, {'pdf', 'dPDF_dX', 'dPDF_dX2'})
    sumP = sum(pi_ * PDF, 0)
    logPDF = log(sumP)
    dLogPDF_dX = sum(pi_*dPDF_dX, 0) / sumP
    dLogPDF_dX2 = ((sum(pi_ * dPDF_dX2, 0) * sumP) - (sum(pi_ * dPDF_dX, 0)) ** 2) / ((sumP) ** 2)
    return logPDF, dLogPDF_dX, dLogPDF_dX2