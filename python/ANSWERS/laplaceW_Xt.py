from numpy import *
from logW_Xt_gradient2 import logW_Xt_gradient2

def dist2(X,Y):
    distMat = nan * ones((X.shape[0], Y.shape[0]))
    for i in range(X.shape[0]):
        for j in range(Y.range[0]):
            distMat[i][j] = sqrt(sum((X[i] - Y[j]) ** 2))


def laplaceW_Xt (X_in,t_in,distFun_in, distPara_array_in,pi_array_in, withSpatial=1,slopePrior=array(())):
    global X,t, distFun, distPara_array, pi_array, muW1, muW2, lamW1, lamW2
    X = round(X_in)
    t = array((t_in,ones(1,len(t_in))))
    distFun = distFun_in
    distPara_array = distPara_array_in
    pi_array = pi_array_in
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
    delete(loc, 25, axis=0)
    delete(loc, 34, axis=0)
    delete(SFR, 25, axis=0)
    delete(SFR, 34, axis=0)
    distMat = dist2(loc, loc)
    angDisMat = sqrt(dist2(SFR.T, SFR.T))
    angDisMat[angDisMat > pi] = 2 * pi - angDisMat(angDisMat > pi)
    angDisMat = angDisMat**2
    if slopePrior.size == 0:
        muW1 = zeros(size(X,0),1)
        A1 = 10
    else:
        muW1 = slopePrior(1) * ones(size(X, 0),1)
        A1 = slopePrior(2)
    muW2 = median(X, 1)
    A2 = 10
    L = 6
    angL = 15 * pi / 180
    distMat1 = A1 ** 2 * exp(-0.5 * (0.5 * distMat / L ** 2 + 0.5 * angDisMat / angL ** 2))
    distMat2 = A2 ** 2 * exp(-0.5 * (0.5 * distMat / L ** 2 + 0.5 * angDisMat / angL ** 2))
    if not withSpatial:
        distMat1 = diag(diag(distMat1))
        distMat2 = diag(diag(distMat2))
    distMat1[0: 25, 26: 51] = 0
    distMat1[26: 51, 0: 25] = 0
    distMat2[0: 25, 26: 51] = 0
    distMat2[26: 51, 0: 25] = 0
    lamW1 = linalg.inv(distMat1)
    lamW2 = linalg.inv(distMat2)

    '''
    options = foptions;
    options(1) = 0;
    options(9) = 0;
    options(14) = 300;
    '''

    oldW = array((zeros(1, 52),median(X,2).T))

    '''
    options = optimoptions('fminunc','GradObj','on','Algorithm','trust-region','DerivativeCheck', 'off', 'Diagnostics', 'off', 'Display', 'off', 'MaxIter', 400);
    [newW] = fminunc('logW_Xt_with_grad',oldW(:)',options);
    newW = reshape(newW, 2, []);
    gradW2 = logW_Xt_gradient2(newW(:));
    '''


    return newW, gradW2