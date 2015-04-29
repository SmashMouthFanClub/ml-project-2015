%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% plotCost.m
% This function plots the cost J after collaborative filtering learning,
% setting the number of features, lambda, root mean squared error, and
% learning time total as the title of the plot.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function plotCost(info)

indexes = [1:info.iterations];
plot(indexes, info.costJ);

title_str = ...
  sprintf("Features = %d, Lambda = %d, RMSE = %f, Time = %ds", ...
          info.num_features, info.lambda, info.rmse, info.t_total);
title(title_str);
xlabel("Iteration #");
ylabel("Cost J");

end
