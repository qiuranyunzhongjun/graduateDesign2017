from numpy import *

def  weibull(x, para, mode=['pdf']):

	paraDim, mixNum = para.shape
	N = x.shape[1]
	PDF = nan * ones((mixNum, N))
	logPDF = nan * ones((mixNum, N))
	dLogPDF_dPara = nan * ones((mixNum, N, paraDim))
	dLogPDF_dX_dPara = nan * ones((mixNum, N, paraDim))
	dLogPDF_dX = nan*ones((mixNum, N))
	dLogPDF_dX2 = nan*ones((mixNum, N))
	
	out1 = array(())
	out2 = array(())
	out3 = array(())
	
	for i in range(len(mode)):
		for mNum in range(len(mixNum))
			k = para[0][mNum]
			r = para[1][mNum]
			u = 0
			
	return out1, out2, out3