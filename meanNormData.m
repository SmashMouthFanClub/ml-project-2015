%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% meanNormData.m
% Normalize the data by subtracting the mean from each movie rating
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [Ynorm, Ymean] = meanNormData(Y, R)

% get the size of the data matrix
[m, n] = size(Y);

% save the mean and normalized data
Ymean = zeros(m, 1);
Ynorm = zeros(size(Y));

for i = 1 : m
    Ymean(i) = mean(Y(i, R(i, :)));
    Ynorm(i, R(i, :)) = Y(i, R(i, :)) - Ymean(i);
end

end
