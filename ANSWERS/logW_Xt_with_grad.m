function [logW,gradW]  = logW_Xt_with_grad(vecW)
%log p(W_n|X_n, t_n)
global X t distFun distPara_array pi_array muW1 muW2 lamW1 lamW2;
[xDim, serialLength] = size(X);
tDim = size(t,1);
W = reshape(vecW, [tDim, xDim]);
logWeibullMix = ones(size(X));
logWeibullMix_grad = ones(size(X));
prediction = W'*t;
negativePredictionInd = find(prediction<2);
prediction(negativePredictionInd) = exp(prediction(negativePredictionInd)-1-1)+1;
for i=1:size(distPara_array,2)
    ind = round(X)==i;
    [logWeibullMix(ind), logWeibullMix_grad(ind)] = logMixtureDist(prediction(ind)', distFun, reshape(distPara_array(:,i),2,[]), pi_array(:,i));
end
logW = -(sum(logWeibullMix(:))-0.5*(W(1,:)*lamW1*W(1,:)')+(W(1,:)*lamW1*muW1)-0.5*(W(2,:)*lamW2*W(2,:)')+(W(2,:)*lamW2*muW2));

T = repmat(t(1,:),xDim,1);
pred_gradW1 = T;
pred_gradW1(negativePredictionInd) = pred_gradW1(negativePredictionInd).*(prediction(negativePredictionInd)-1);
%gradWW1 = zeros(size(X));
%gradWW1(negativePredictionInd) = (prediction(negativePredictionInd)-1).*T(negativePredictionInd).^2;

T = repmat(t(2,:),xDim,1);
pred_gradW2 = T;
pred_gradW2(negativePredictionInd) = pred_gradW2(negativePredictionInd).*(prediction(negativePredictionInd)-1);
%gradWW2 = zeros(size(X));
%gradWW2(negativePredictionInd) = (prediction(negativePredictionInd)-1).*T(negativePredictionInd).^2;

grad1_1 = sum(logWeibullMix_grad.*pred_gradW1,2)-lamW1*W(1,:)'+lamW1*muW1;
grad1_2 = sum(logWeibullMix_grad.*pred_gradW2,2)-lamW2*W(2,:)'+lamW2*muW2;
gradW = [grad1_1'; grad1_2'];
gradW = -gradW(:)';

% logWeibullMix_grad = repmat(logWeibullMix_grad, [1,1,tDim]).*repmat(permute(t,[3,2,1]),[xDim, 1, 1]);
% grad_1 = logWeibullMix_grad(:,:,1);
% grad_1(negativePredictionInd) = grad_1(negativePredictionInd).*(prediction(negativePredictionInd)-1);
% grad_1 = sum(grad_1, 2)-lamW1*W(1,:)'+lamW1*muW1;
% grad_2 = logWeibullMix_grad(:,:,2);
% grad_2(negativePredictionInd) = grad_2(negativePredictionInd).*(prediction(negativePredictionInd)-1);
% grad_2 = sum(grad_2, 2)-lamW2*W(2,:)'+lamW2*muW2;
% gradW = [grad_1'; grad_2'];
% gradW = -gradW(:);