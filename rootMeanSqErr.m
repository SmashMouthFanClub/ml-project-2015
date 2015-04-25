%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% rootMeanSqErr.m
% This function calculates the root mean squared error of the
% recommender system.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function rmse = rootMeanSqErr(Y, recom)

%%%% TODO: sum or size for Y?
rmse = sqrt(sum((Y(:) .- recom(:)).^2) / sum(Y(:), 1));

end
