function [newW gradW2] = laplaceW_Xt(X_in,t_in,distFun_in, distPara_array_in,pi_array_in, withSpatial,slopePrior)
if exist('withSpatial')~=1
    withSpatial = 1;
end
global X t distFun distPara_array pi_array muW1 muW2 lamW1 lamW2;
X = round(X_in);
t = [t_in; ones(1,length(t_in))];
distFun = distFun_in;
distPara_array = distPara_array_in;
pi_array = pi_array_in;
loc = [ [ -9, 21 ]; [ -3, 21 ];
    [ 3, 21 ]; [ 9, 21 ]; [ -15, 15 ]; [ -9, 15 ]; [ -3, 15 ];
    [ 3, 15 ]; [ 9, 15 ]; [ 15, 15 ]; [ -21, 9 ]; [ -15, 9 ];
    [ -9, 9 ]; [ -3, 9 ]; [ 3, 9 ]; [ 9, 9 ]; [ 15, 9 ]; [ 21, 9 ];
    [ -27, 3 ]; [ -21, 3 ]; [ -15, 3 ]; [ -9, 3 ]; [ -3, 3 ]; [ 3, 3 ];
    [ 9, 3 ]; [ 15, 3 ]; [ 21, 3 ]; [ -27, -3 ]; [ -21, -3 ];
    [ -15, -3 ]; [ -9, -3 ]; [ -3, -3 ]; [ 3, -3 ]; [ 9, -3 ];
    [ 15, -3 ]; [ 21, -3 ]; [ -21, -9 ]; [ -15, -9 ]; [ -9, -9 ];
    [ -3, -9 ]; [ 3, -9 ]; [ 9, -9 ]; [ 15, -9 ]; [ 21, -9 ];
    [ -15, -15 ]; [ -9, -15 ]; [ -3, -15 ]; [ 3, -15 ]; [ 9, -15 ];
    [ 15, -15 ]; [ -9, -21 ]; [ -3, -21 ]; [ 3, -21 ]; [ 9, -21 ] ];
SFR = pi-[268 262 252 245 264 274 281 275 260 246 271 285 291 296 298 283 253 229 278 287 291 298 312 329 318 1 218 83 76 68 55 34 11 13 1 167 85 78 66 56 48 60 95 136 88 81 77 80 93 112 93 95 100 108]*pi/180.0;
loc([26,35],:) = [];
SFR([26,35]) = [];
distMat = dist2(loc, loc);
angDisMat = sqrt(dist2(SFR', SFR'));
angDisMat(angDisMat>pi) = 2*pi-angDisMat(angDisMat>pi);
angDisMat = angDisMat.^2;

if isempty(slopePrior)
    muW1 = zeros(size(X,1),1);
    A1 = 10;
else
    muW1 = slopePrior(1)*ones(size(X,1),1);
    A1 = slopePrior(2);
end
muW2 = median(X,2);
A2 = 10;

L = 6; angL = 15*pi/180;
%distMat = A^2.*exp(-0.5*(0.5*distMat/L^2+0.5*angDisMat/angL^2));
distMat1 = A1^2*exp(-0.5*(0.5*distMat/L^2+0.5*angDisMat/angL^2));
distMat2 = A2^2*exp(-0.5*(0.5*distMat/L^2+0.5*angDisMat/angL^2));
if ~withSpatial
    distMat1 = diag(diag(distMat1));%!!!!!!ST filter disabled
    distMat2 = diag(diag(distMat2));%!!!!!!ST filter disabled
end
distMat1(1:26, 27:52) = 0;
distMat1(27:52, 1:26) = 0;
distMat2(1:26, 27:52) = 0;
distMat2(27:52, 1:26) = 0;
lamW1 = inv(distMat1);
lamW2 = inv(distMat2);

%[slop, intercept] = LRRegression(X_in, t_in);
% muW1 = slop;
% muW2 = intercept;

options = foptions;
options(1) = 0;
options(9) = 0;
options(14) = 300;
oldW = [zeros(1, 52); median(X,2)'];
%oldW = [slop'; intercept'];
%[newW, options] = scg('logW_Xt', oldW(:)', options, 'logW_Xt_gradient');
options = optimoptions('fminunc','GradObj','on','Algorithm','trust-region','DerivativeCheck', 'off', 'Diagnostics', 'off', 'Display', 'off', 'MaxIter', 400);
[newW] = fminunc('logW_Xt_with_grad',oldW(:)',options);
% score = options(8);
% oldW = [zeros(1, 52); ones(1,52)+1/exp(1)];
% [tempNewW, options] = scg('logW_Xt', oldW(:)', options, 'logW_Xt_gradient');
% if (options(8)<score)
%     newW = tempNewW;
% end
newW = reshape(newW, 2, []);

gradW2 = logW_Xt_gradient2(newW(:));