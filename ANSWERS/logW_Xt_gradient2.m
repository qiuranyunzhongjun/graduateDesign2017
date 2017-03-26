function [gradW2]  = logW_Xt_gradient2(vecW)
%log p(W_n|X_n, t_n)
global X t distFun distPara_array pi_array muW1 muW2 lamW1 lamW2;
[xDim, serialLength] = size(X);
tDim = size(t,1);
W = reshape(vecW, [tDim, xDim]);
logWeibullMix = ones(size(X));
logWeibullMix_grad = ones(size(X));
logWeibullMix_grad2 = ones(size(X));
prediction = W'*t;
negativePredictionInd = find(prediction<2);
prediction(negativePredictionInd) = exp(prediction(negativePredictionInd)-1-1)+1;
for i=1:size(distPara_array,2)
    ind = round(X)==i;
    [logWeibullMix(ind), logWeibullMix_grad(ind), logWeibullMix_grad2(ind)] = logMixtureDist(prediction(ind)', distFun, reshape(distPara_array(:,i),2,[]), pi_array(:,i));
end
%logW = -(sum(logWeibullMix(:))-0.5*(W(1,:)*lamW1*W(1,:)')+(W(1,:)*lamW1*muW1)-0.5*(W(2,:)*lamW2*W(2,:)')+(W(2,:)*lamW2*muW2));

T1 = repmat(t(1,:),xDim,1);
T2 = repmat(t(2,:),xDim,1);
pred_gradW1 = T1;
pred_gradW1(negativePredictionInd) = T1(negativePredictionInd).*(prediction(negativePredictionInd)-1);
pred_gradWW1 = zeros(size(X));
pred_gradWW1(negativePredictionInd) = (prediction(negativePredictionInd)-1).*T1(negativePredictionInd).^2;
pred_gradW1W2 = zeros(size(X));
pred_gradW1W2(negativePredictionInd) = (prediction(negativePredictionInd)-1).*T1(negativePredictionInd).*T2(negativePredictionInd);

pred_gradW2 = T2;
pred_gradW2(negativePredictionInd) = T2(negativePredictionInd).*(prediction(negativePredictionInd)-1);
pred_gradWW2 = zeros(size(X));
pred_gradWW2(negativePredictionInd) = (prediction(negativePredictionInd)-1).*T2(negativePredictionInd).^2;

% grad1_1 = sum(logWeibullMix_grad.*pred_gradW1,2)-lamW1*W(1,:)'+lamW1*muW1;
% grad1_2 = sum(logWeibullMix_grad.*pred_gradW2,2)-lamW2*W(2,:)'+lamW2*muW2;

grad2_1 = logWeibullMix_grad2.*pred_gradW1.^2+logWeibullMix_grad.*pred_gradWW1;
grad2_1 = diag(sum(grad2_1, 2))-lamW1;

grad2_12 = logWeibullMix_grad2.*pred_gradW1.*pred_gradW2+logWeibullMix_grad.*pred_gradW1W2;
grad2_12 = diag(sum(grad2_12, 2));

grad2_2 = logWeibullMix_grad2.*pred_gradW2.^2+logWeibullMix_grad.*pred_gradWW2;
grad2_2 = diag(sum(grad2_2, 2))-lamW2;

gradW2 = zeros(xDim, xDim, 3);
gradW2(:,:,1) = grad2_1;
gradW2(:,:,2) = grad2_2;
gradW2(:,:,3) = grad2_12;
%gradW2 = -gradW2;
% gradW = [grad_1'; grad_2'];
% gradW = -gradW(:);