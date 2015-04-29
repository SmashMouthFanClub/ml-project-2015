%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% rootMeanSqErr.m
% This function calculates the root mean squared error of the
% recommender system.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function rmse = rootMeanSqErr(Y, recom, R)

%%%% TODO: sum or size for Y? or use R? or wat?
rmse = sqrt(sum((R(:).*(Y(:) .- recom(:))).^2) / sum(R(:), 1));

% Below: MAE metric instead (doesn't square errors, i.e. being off by
% 2 stars doesn't penalize you by 4)
%rmse = sum(abs(Y(:) .- recom(:))) / sum(Y(:), 1);

end
