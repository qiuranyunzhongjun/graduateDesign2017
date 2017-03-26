function [out1, out2, out3] =  weibull(x, para, mode)
% mode can be: pdf, logpdf, d_x, d_para
if nargin<3
    mode = {'pdf'};
end
[paraDim, mixNum] = size(para);
N = size(x, 2);
PDF = nan*ones(mixNum, N);
logPDF = nan*ones(mixNum, N);
dLogPDF_dPara = nan*ones(mixNum, N, paraDim);
dLogPDF_dX_dPara = nan*ones(mixNum, N, paraDim);
dLogPDF_dX = nan*ones(mixNum, N);
dLogPDF_dX2 = nan*ones(mixNum, N);

out1=[];
out2=[];
out3=[];
for i=1:length(mode)
    %negXInd = find(x<=0);
    for mNum=1:mixNum
        k = para(1,mNum);%shape
        r = para(2,mNum);%location
        u = 0;%center
        
        % syms x k r f;
        % f = (k/r)*(x./r).^(k-1)*exp(-(x./r).^k);
        % simplify(diff(log(f), k), 'IgnoreAnalyticConstraints', true);
        if strcmp(mode{i},'pdf')==1
            PDF(mNum,:) = (k/r)*((x-u)./r).^(k-1).*exp(-((x-u)./r).^k);
        end
        if strcmp(mode{i},'logpdf')==1
            logPDF(mNum,:) = log(k/r)+(k-1)*log((x-u)./r)-((x-u)./r).^k;
        end
        
        if strcmp(mode{i},'dPDF_dX')==1
            dPDF_dX(mNum,:) = -(k*(-(u - x)./r).^k.*(k*(-(u - x)./r).^k - k + 1))./(exp((-(u - x)./r).^k).*(u - x).^2);
%             d2PDF_dX2(mNum,:) = -(k*(-(u - x)./r).^k.*(k^2*(-(u - x)./r).^(2*k) - 3*k + 3*k.*(-(u - x)./r).^k + k^2 - 3*k^2.*(-(u - x)./r).^k + 2))./(exp((-(u - x)./r).^k).*(u - x).^3);
%             dLogPDF_dX(mNum,:) = - (k - 1)./(u - x) - (k.*(-(u - x)./r).^(k - 1))./r;
            %dLogPDF_dX2(mNum,:) = -(k*(-(u - x)./r).^k.*(k^2*(-(u - x)./r).^(2*k) - 3*k + 3*k.*(-(u - x)./r).^k + k^2 - 3*k^2.*(-(u - x)./r).^k + 2))./(exp((-(u - x)./r).^k).*(u - x).^3);
        end
        
        if strcmp(mode{i},'dPDF_dX2')==1
%             dPDF_dX(mNum,:) = -(k*(-(u - x)./r).^k.*(k*(-(u - x)./r).^k - k + 1))./(exp((-(u - x)./r).^k).*(u - x).^2);
            dPDF_dX2(mNum,:) = -(k*(-(u - x)./r).^k.*(k^2*(-(u - x)./r).^(2*k) - 3*k + 3*k.*(-(u - x)./r).^k + k^2 - 3*k^2.*(-(u - x)./r).^k + 2))./(exp((-(u - x)./r).^k).*(u - x).^3);
%             dLogPDF_dX(mNum,:) = - (k - 1)./(u - x) - (k.*(-(u - x)./r).^(k - 1))./r;
            %dLogPDF_dX2(mNum,:) = -(k*(-(u - x)./r).^k.*(k^2*(-(u - x)./r).^(2*k) - 3*k + 3*k.*(-(u - x)./r).^k + k^2 - 3*k^2.*(-(u - x)./r).^k + 2))./(exp((-(u - x)./r).^k).*(u - x).^3);
        end
        
        if strcmp(mode{i},'dLogPDF_dX')==1
%             dPDF_dX(mNum,:) = -(k*(-(u - x)./r).^k.*(k*(-(u - x)./r).^k - k + 1))./(exp((-(u - x)./r).^k).*(u - x).^2);
%             d2PDF_dX2(mNum,:) = -(k*(-(u - x)./r).^k.*(k^2*(-(u - x)./r).^(2*k) - 3*k + 3*k.*(-(u - x)./r).^k + k^2 - 3*k^2.*(-(u - x)./r).^k + 2))./(exp((-(u - x)./r).^k).*(u - x).^3);
            dLogPDF_dX(mNum,:) = - (k - 1)./(u - x) - (k.*(-(u - x)./r).^(k - 1))./r;
            %dLogPDF_dX2(mNum,:) = -(k*(-(u - x)./r).^k.*(k^2*(-(u - x)./r).^(2*k) - 3*k + 3*k.*(-(u - x)./r).^k + k^2 - 3*k^2.*(-(u - x)./r).^k + 2))./(exp((-(u - x)./r).^k).*(u - x).^3);
        end
        %dLogPDF_dU = (k*((x-u)./r).^k - k + 1)./(x-u);
        
        if strcmp(mode{i},'dLogPDF_dPara')==1
            dLogPDF_dK = 1/k - (log(x-u)-log(r)).*(((x-u)./r).^k - 1);
            dLogPDF_dR = (k*(((x-u)./r).^k - 1))/r;
            dLogPDF_dPara(mNum,:,1) = dLogPDF_dK;
            dLogPDF_dPara(mNum,:,2) = dLogPDF_dR;
        end
        
        if strcmp(mode{i},'dLogPDF_dX_dPara')==1
            dLogPDF_dX_dK = 1/k - (log(x-u)-log(r)).*(((x-u)./r).^k - 1);
            dLogPDF_dX_dR = (k*(((x-u)./r).^k - 1))/r;
            dLogPDF_dX_dPara(mNum,:,1) = dLogPDF_dX_dK;
            dLogPDF_dX_dPara(mNum,:,2) = dLogPDF_dX_dR;
        end
        %dLogPDF_dPara(i,:,3) = dLogPDF_dU;
    end
    
    out = [];
    switch mode{i}
        case 'pdf'
           out = PDF;
        case 'logpdf'
           out = logPDF;
        case 'dPDF_dX'
            out = dPDF_dX;
        case 'dPDF_dX2'
            out = dPDF_dX2;
        case 'dLogPDF_dX'
            out = dLogPDF_dX;
        case 'dLogPDF_dPara'
            out = dLogPDF_dPara;
        case 'dLogPDF_dX_dPara'
            out = dLogPDF_dX_dPara;
    end
    
    switch i
        case 1
            out1 = out;
        case 2
            out2 = out;
        case 3
            out3 = out;
    end
end

% switch mode
%     case 'pdf'
%         out1=PDF;
%         out2 = logPDF;
%     case 'gradient'
%         out1=dLogPDF_dPara;
%     case 'both'
%         out1=PDF;
%         out2 = logPDF;
%         out3=dLogPDF_dPara;
%     case 'gradientX'
%         out1=PDF;
%         out2 = dPDF_dX;
%         out3 = d2PDF_dX2;
% end
