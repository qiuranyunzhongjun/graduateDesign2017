function [slop, intercept, slopSD, interceptSD] = STRegression(X, t, distPara_array, pi_array, withSpatial, slopePrior)
if exist('withSpatial')~=1
    withSpatial = 1;
end
% spatio-temporal regression
[w, gradW2] = laplaceW_Xt(X,t,'weibull',distPara_array,pi_array,withSpatial,slopePrior);
slop = w(1,:)';
intercept = w(2,:)';

% slopSD = sqrt(-1./diag(gradW2(:,:,1)));
% interceptSD = sqrt(-1./diag(gradW2(:,:,2)));

%slopSD = sqrt(-diag(inv(gradW2(:,:,1))));
%interceptSD = sqrt(-diag(inv(gradW2(:,:,2))));

SD = sqrt(-diag(inv([[gradW2(:,:,1),gradW2(:,:,3)];[gradW2(:,:,3),gradW2(:,:,2)]])));
slopSD = SD(1:52);
interceptSD = SD(53:104);