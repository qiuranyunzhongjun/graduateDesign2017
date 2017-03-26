function [logPDF, dLogPDF_dX, dLogPDF_dX2] = logMixtureDist(x, distFun, distPara, pi_)
%gradientX: gradient of logPDF w.r.t. x 
%N = size(x, 2);
[PDF, dPDF_dX, dPDF_dX2] = feval(distFun, x, distPara, {'pdf', 'dPDF_dX', 'dPDF_dX2'});
sumP = sum(bsxfun(@times,pi_,PDF),1);
logPDF = log(sumP);
dLogPDF_dX = sum(bsxfun(@times,pi_,dPDF_dX),1)./sumP;
dLogPDF_dX2 = ((sum(bsxfun(@times,pi_,dPDF_dX2),1).*sumP)-...
    (sum(bsxfun(@times,pi_,dPDF_dX),1)).^2)./((sumP).^2);
%gradientXX = -gradientX.^2+(1./sumP).*sum(bsxfun(@times,pi_,d2PDF_dX2),1);