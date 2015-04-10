%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% mainDriver.m
% This file will load the movies, perform learning, and output the top
% movie recommendations for a given user.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%% TODO - Divide the data into training/CV/test and perform
%%%%%      - appropriate cross-validation and tests, reporting stats for
%%%%%      - how well our predictions perform.
clc; close all; clear;

% data matrix and movie title file locations
f_movie_matrix = 'data/movies.mat';
f_movie_titles = 'data/movie_titles.txt';

% load in movie rating data
plush('\nLoading movie rating data...\n');

% this will load a matrix Y containing movie ratings where the rows
% are movies and columns are users
load(f_movie_matrix);
plush('...complete.\n\n');

% load in movie titles
plush('Matching movie IDs to titles...\n');
map_id_name = loadMovieIDNameMap(f_movie_titles);
plush('...complete.\n\n');

% add a new user's ratings to the system
new_ratings = zeros(size(Y, 1), 1);
new_ratings(1)   = 4;
new_ratings(7)   = 3;
new_ratings(12)  = 5;
new_ratings(54)  = 4;
new_ratings(64)  = 5;
new_ratings(66)  = 3;
new_ratings(69)  = 5;
new_ratings(98)  = 2;
new_ratings(183) = 4;
new_ratings(226) = 5;
new_ratings(355) = 5;

plush('You rated:\n');
for i = 1 : length(new_ratings)
    if (new_ratings(i) > 0)
        fprintf('\t%.1f for %s\n', ...
                new_ratings(i), map_id_name{i});
    end
end
plush('\n');

% use collaborative filtering to train the model on the movie rating data
plush('Using fmincg to train collaborative filtering model...\n');

% add the new ratings to the data
Y = [new_ratings Y];

% map R(i,j) to 1 if Y(i,j) is > 0, and 0 otherwise
R = (Y > 0);

% perform mean normalization
[Y_norm, Y_mean] = meanNormData(Y, R);

% initialize the number of features to use, regularization parameter,
% and number of iterations to train with
num_features = 30;
lambda = 10;
iterations = 100;

printf('\tFeature count: %d\n', num_features);
printf('\tLambda:        %d\n', lambda);
printf('\tIterations:    %d\n', iterations);
plush('');

% number of movies are rows, number of users are columns
num_movies = size(Y, 1);
num_users = size(Y, 2);

% randomly initialize X and Theta to small values for collab. filtering
X = randn(num_movies, num_features);
Theta = randn(num_users, num_features);

% fold the parameters into a single row vector
initial_params = [X(:); Theta(:)];

%%%%% TODO - test lambda and iteration and num_features values
%%%%%      - once we get new data in to find best performance

%%%%% TODO - why does training on Y_norm and adding back Y_mean
%%%%%      - only recommend the best rated movies?
%%%%% - answer: because Y_mean = 5 when only 1 user rated 1
%%%%% -         movie a 5.

%%%%% TODO - maybe we weight each rating by the number of users
%%%%%      - that rated that movie

% set options for fmincg (including iterations) and run the training
%%%%% TODO - report stats on training on Y vs Y_norm
t_start = time();  %%%%% TODO - try fminunc with TolFun
options = optimset('GradObj', 'on', 'MaxIter', iterations);
[thetafold, costJ] = fmincg (@(t)(collabFilter(t, Y_norm, R, num_users, ...
                                  num_movies, num_features, lambda)), ...
                     initial_params, options);
fprintf('Training took %d seconds.\n', time() - t_start);

% unfold the returned values
X = reshape(thetafold(1:num_movies*num_features), num_movies, num_features);
Theta = reshape(thetafold(num_movies*num_features+1:end), ...
                num_users, num_features);

plush('...complete.\n\n');

% get the recommendation matrix
recom_matrix = X * Theta';

% plot the cost by iteration
indexes = [1:iterations];
plot(indexes, costJ ./ costJ(1));
title("Error Per Iteration");
xlabel("Iteration #");
ylabel("Cost J");

% use SVD to reduce the dimensionality of the matrix
plush('Dimensionality reduction with SVD...\n');
[recom_matrix, Y_mean] = svdReduce(recom_matrix, Y_mean);
plush('...complete.\n\n');

% make a prediction for the user
pred = recom_matrix(:,1) + Y_mean;

% sort the vector to get the highest rating movies first
[x, ix] = sort(pred, 'descend');

%%%%% TODO - threshold to 0 the movies the user already watched

% print top 10 recommendations
plush('Our top 10 recommendations for you:\n');
for i = 1 : 10 % length(pred)
    j = ix(i);
    fprintf('\t%.1f for %s\n', pred(j), map_id_name{j});
end

% get root-mean-squared-deviation error in comparison
plush('\nGenerating RMSD error: ');
rmse = sqrt(sum((Y(:) .- recom_matrix(:)).^2) / size(Y(:),1));
printf("%f%%\n", rmse);
printf("Netflix 2006 RMSD error: 0.9525%%\n");

plush('\n');
