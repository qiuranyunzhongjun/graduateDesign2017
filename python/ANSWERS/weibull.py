from numpy import *


def weibull(x, para, mode=['pdf']):
    paraDim, mixNum = para.shape
    if x.ndim == 1:
        N = x.shape[0]
    else:
        N = x.shape[1]
    PDF = nan * ones((mixNum, N))
    logPDF = nan * ones((mixNum, N))
    dPDF_dX = nan * ones((mixNum, N))
    dPDF_dX2 = nan * ones((mixNum, N))
    dLogPDF_dPara = nan * ones((paraDim, mixNum, N))
    dLogPDF_dX_dPara = nan * ones((paraDim, mixNum, N))
    dLogPDF_dX = nan * ones((mixNum, N))
    dLogPDF_dX2 = nan * ones((mixNum, N))

    out1 = array(())
    out2 = array(())
    out3 = array(())

    for i in range(len(mode)):
        for mNum in range(mixNum):

            k = para[0][mNum]
            r = para[1][mNum]
            u = 0
            if mode[i] == 'pdf':
                PDF[mNum] = (k / r) * ((x - u) / r) ** (k - 1) * exp(-((x - u) / r) ** k)
            if mode[i] == 'logpdf':
                logPDF[mNum] = log(k / r) + (k - 1) * log((x - u) / r) - ((x - u) / r) ** k
            if mode[i] == 'dPDF_dX':
                dPDF_dX[mNum] = -(k * (-(u - x) / r) ** k * (k * (-(u - x) / r) ** k - k + 1)) / (
                exp((-(u - x) / r) ** k) * (u - x) ** 2)
            if mode[i] == 'dPDF_dX2':
                dPDF_dX2[mNum] = -(k * (-(u - x) / r) ** k * (
                k ** 2 * (-(u - x) / r) ** (2 * k) - 3 * k + 3 * k * (-(u - x) / r) ** k + k ** 2 - 3 * k ** 2 * (
                -(u - x) / r) ** k + 2)) / (exp((-(u - x) / r) ** k) * (u - x) ** 3)
            if mode[i] == 'dLogPDF_dX':
                dLogPDF_dX[mNum] = - (k - 1) / (u - x) - (k * (-(u - x) / r) ** (k - 1)) / r
            if mode[i] == 'dLogPDF_dPara':
                dLogPDF_dK = 1 / k - (log(x - u) - log(r)) * (((x - u) / r) ** k - 1)
                dLogPDF_dR = (k * (((x - u) / r) ** k - 1)) / r
                dLogPDF_dPara[0][mNum] = dLogPDF_dK
                dLogPDF_dPara[1][mNum] = dLogPDF_dR
            if mode[i] == 'dLogPDF_dX_dPara':
                dLogPDF_dX_dK = 1 / k - (log(x - u) - log(r)) * (((x - u) / r) ** k - 1)
                dLogPDF_dX_dR = (k * (((x - u) / r) ** k - 1)) / r
                dLogPDF_dX_dPara[0][mNum] = dLogPDF_dX_dK
                dLogPDF_dX_dPara[1][mNum] = dLogPDF_dX_dR

        out = array(())
        if mode[i] == 'pdf':
            out = PDF
        elif mode[i] == 'logpdf':
            out = logPDF
        elif mode[i] == 'dPDF_dX':
            out = dPDF_dX
        elif mode[i] == 'dPDF_dX2':
            out = dPDF_dX2
        elif mode[i] == 'dLogPDF_dX':
            out = dLogPDF_dX
        elif mode[i] == 'dLogPDF_dPara':
            out = dLogPDF_dPara
        elif mode[i] == 'dLogPDF_dX_dPara':
            out = dLogPDF_dX_dPara

        if i == 0:
            out1 = out
        elif i == 1:
            out2 = out
        elif i == 2:
            out3 = out

    return out1, out2, out3


if __name__ == "__main__":
    x = array([0.1, 0.2, 0.3])
    para = array([[1, 2], [3, 4]])
    mode = ['pdf', 'dPDF_dX', 'dPDF_dX2']
    [o1, o2, o3] = weibull(x, para, mode)
    print(o1)
    print(o2)
    print(o3)