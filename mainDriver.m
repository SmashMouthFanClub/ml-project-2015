%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% mainDriver.m
% This file will load the movies, perform learning, and output the top
% movie recommendations for a given user.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% data matrix and movie title file locations
f_movie_matrix = 'data/movies.mat';
f_movie_titles = 'data/movie_titles.txt';

% load in movie rating data
plush('\nLoading movie rating data...\n');

% this will load a matrix Y containing movie ratings where the rows
% are movies and columns are users
load(f_movie_matrix);

% map R(i,j) to 1 if Y(i,j) is > 0, and 0 otherwise
R = (Y > 0);

plush('...complete.\n\n');

% load in movie titles
plush('Matching movie IDs to titles...\n');
map_id_name = loadMovieIDNameMap(f_movie_titles);
plush('...complete.\n\n');

%%%%% TODO - make this part interactive: for now, use Ng's example

% add a new user's ratings to the system
new_ratings = zeros(size(Y, 1), 1);
new_ratings(1) = 4;
new_ratings(7) = 3;
new_ratings(12) = 5;
new_ratings(54) = 4;
new_ratings(64) = 5;
new_ratings(66) = 3;
new_ratings(69) = 5;
new_ratings(98) = 2;
new_ratings(183) = 4;
new_ratings(226) = 5;
new_ratings(355) = 5;

plush('You rated:\n');
for i = 1 : length(new_ratings)
    if new_ratings(i) > 0
        fprintf('\t%.1f for %s\n', ...
                 new_ratings(i), map_id_name{i});
    end
end
plush('\n');

%%%%% END TODO - make this part interactive

% use collaborative filtering to train the model on the movie rating data
plush('Using fmincg to train collaborative filtering model...\n');

% add the new ratings to the data
Y = [new_ratings Y];
R = [(new_ratings ~= 0) R];

% perform mean normalization
[Y_norm, Y_mean] = meanNormData(Y, R);

% initialize the number of features to use, regularization parameter,
% and number of iterations to train with
num_features = 10;
lambda = 10;
iterations = 100;

% number of movies are rows, number of users are columns
num_movies = size(Y, 1);
num_users = size(Y, 2);

% randomly initialize X and Theta to small values for collab. filtering
X = randn(num_movies, num_features);
Theta = randn(num_users, num_features);

%%%%% TODO - do we realllyyyyy need to be folding/unfolding?
% fold the parameters into a single row vector
initial_params = [X(:); Theta(:)];

%%%%% TODO - test lambda and iteration and num_features values

% set options for fmincg (including iterations) and run the training
% on the normalized Y values
t_start = time();  %%%%% TODO - try fminunc with TolFun
options = optimset('MaxIter', iterations); %('TolFun', 0.0001);
theta = fmincg (@(t)(collabFilter(t, Y_norm, R, num_users, num_movies, ...
                                  num_features, lambda)), ...
                     initial_params, options);
fprintf('Training took %d seconds.\n', time() - t_start);

% unfold the returned values
X = reshape(theta(1:num_movies*num_features), num_movies, num_features);
Theta = reshape(theta(num_movies*num_features+1:end), ...
                num_users, num_features);

plush('...complete.\n\n');

% make the user's recommendation
recom_matrix = X * Theta';
pred = recom_matrix(:,1) + Y_mean;

% sort the vector to get the highest rating movies first
[x, ix] = sort(pred, 'descend');

% print top 10 recommendations
plush('Our top 10 recommendations for you:\n');
for i = 1 : 10
    j = ix(i);
    fprintf('\t%.1f for %s\n', pred(j), map_id_name{j});
end

plush('\n');
