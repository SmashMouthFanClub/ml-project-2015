%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% collabFilter.m
% This file performs the collaborative filtering cost function, and
% returns the cost and gradient.  Both X and Theta are updated
% simultaneously in collaborative filtering.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [J, grad] = collabFilter(params, Y, R, num_users, num_movies, ...
                                  num_features, lambda)

% Unfold the X and Theta matrices
X = reshape(params(1:num_movies*num_features), num_movies, num_features);
Theta = reshape(params(num_movies*num_features+1:end), ...
                num_users, num_features);
    
% compute the cost, J
J = (1 / 2) * sum(sum(R .* (X * Theta' - Y) .^ 2)) + ...
	(lambda / 2) * (sum(sum(Theta .^ 2)) + sum(sum(X .^ 2)));

% initialize X_grad, the matrix of partial derivatives of X
X_grad = zeros(size(X));

% initialize Theta_grad, the matrix of partial derivatives of Theta
Theta_grad = zeros(size(Theta));

% compute X_grad
for i = 1 : num_movies
	% find all users that have rated this movie
    idx = find(R(i, :) == 1);
	% only consider those who have rated the movie
    Theta_rate = Theta(idx, :);
    Y_rate = Y(i, idx);
	% compute the gradient
    X_grad(i, :) = (X(i, :) * Theta_rate' - Y_rate) * ...
		Theta_rate + lambda * X(i, :);
end

% compute Theta_grad
for i = 1 : num_users
	% find all movies rated by this user
    idx = find(R(:, i) == 1);
	% only consider movies rated by the user
    X_rate = X(idx, :);
    Y_rate = Y(idx, i);
	% compute the gradient
    Theta_grad(i, :) = (X_rate * Theta(i, :)' - Y_rate)' * ...
		X_rate + lambda * Theta(i, :);
end

% fold the gradient matrices into one vector
grad = [X_grad(:); Theta_grad(:)];

end
