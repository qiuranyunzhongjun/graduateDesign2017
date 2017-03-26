function [S, pv, slop, intercept, slopSD, interceptSD] = STTrendAnalysis(X, t, distPara_array, pi_array, sigChangPerYear, p_val, withSpatial, slopePrior)
if exist('withSpatial')~=1
    withSpatial = 1;
end
if exist('slopePrior')~=1
    slopePrior = [];
end
adjustedX = X;
% adjustedX = adjustedX-repmat(sigChangPerYear*t, size(X,1), 1);
% for i=1:size(X,2)
%     adjustedX(:,i) = X(:,i)-sigChangPerYear*t(i);
% end
[slop, intercept, slopSD, interceptSD] = STRegression(adjustedX, t, distPara_array, pi_array, withSpatial, slopePrior);
slopSD = abs(slopSD);
pv = slop;
pv(slop>0) = 1-normcdf(0, slop(slop>0), slopSD(slop>0));
pv(slop<=0) = normcdf(0, -slop(slop<=0), slopSD(slop<=0));
%pv = 1-normcdf(0, slop, slopSD);
progressPt = (pv<p_val)&(slop<sigChangPerYear);
progressPt(:)=1;

S = -log(pv).*progressPt;
S(progressPt==0) = 0;
S = sum(S);


% if sum(progressPt)>0
%     if length(progressPt)==52
%         progressPt = [progressPt(1:25);0;progressPt(26:33);0;progressPt(34:end)];
%     end
%     rightEyeLocations = [ [ -9, 21 ]; [ -3, 21 ];
%         [ 3, 21 ]; [ 9, 21 ]; [ -15, 15 ]; [ -9, 15 ]; [ -3, 15 ];
%         [ 3, 15 ]; [ 9, 15 ]; [ 15, 15 ]; [ -21, 9 ]; [ -15, 9 ];
%         [ -9, 9 ]; [ -3, 9 ]; [ 3, 9 ]; [ 9, 9 ]; [ 15, 9 ]; [ 21, 9 ];
%         [ -27, 3 ]; [ -21, 3 ]; [ -15, 3 ]; [ -9, 3 ]; [ -3, 3 ]; [ 3, 3 ];
%         [ 9, 3 ]; [ 15, 3 ]; [ 21, 3 ]; [ -27, -3 ]; [ -21, -3 ];
%         [ -15, -3 ]; [ -9, -3 ]; [ -3, -3 ]; [ 3, -3 ]; [ 9, -3 ];
%         [ 15, -3 ]; [ 21, -3 ]; [ -21, -9 ]; [ -15, -9 ]; [ -9, -9 ];
%         [ -3, -9 ]; [ 3, -9 ]; [ 9, -9 ]; [ 15, -9 ]; [ 21, -9 ];
%         [ -15, -15 ]; [ -9, -15 ]; [ -3, -15 ]; [ 3, -15 ]; [ 9, -15 ];
%         [ 15, -15 ]; [ -9, -21 ]; [ -3, -21 ]; [ 3, -21 ]; [ 9, -21 ] ];
%     X = [-27:6:27];
%     Y = [21:-6:-21];
%     Z = zeros(length(Y),length(X));
% 
%     for i=1:length(rightEyeLocations)
%         Z(find(Y==rightEyeLocations(i,2)),find(X==rightEyeLocations(i,1))) = progressPt(i);
%     end
%     Z(:,size(Z,2)) = [];
%     
%     progress=0;
%     [L,num] = bwlabel(Z,8);
%     for i=1:num
%         if length(find(L==i))>=consecutiveNum
%             progress = 1;
%             break;
%         end
%     end
% else
%     progress = 0;
% end

