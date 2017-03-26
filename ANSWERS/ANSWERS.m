function [S,pnd,slope] = ANSWERS(vf, time)
if size(vf,2)==54
    vf(:, [26,35])=[];
end
vf = vf+1;
load weibull_mixture_para_1offset.mat;
%load weibull_mixture_para_1offset_RAPID_no0_constraint.mat
[S, pnd, slope] = STTrendAnalysis(vf', time, distPara_array, pi_array, -0.0, 1.0, 1);
pnd = pnd';
slope = slope';

%plotANSWERS(vf, pnd, slope, '');
