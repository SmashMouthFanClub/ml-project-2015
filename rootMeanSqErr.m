%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% rootMeanSqErr.m
% This function calculates the root mean squared error of the
% recommender system.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function rmse = rootMeanSqErr(Y, recom)

rmse = sqrt(sum((Y(:) .- recom(:)).^2) / size(Y(:),1));

end
