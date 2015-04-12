%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% svdReduce.m
% This file will use SVD to reduce the dimensionality of the movie
% recommendation matrix.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [recom_svd, Y_svd] = svdReduce(recom_matrix, Y_mean)

%%%%% TODO - Misael
%%%%% - use svd to reduce the dimensionality of the recommendation matrix
%%%%% - passed into the function.  For now, I just return the matrix.
%%%%% - For a good source, see:
%%%%% - http://www.cs.carleton.edu/cs_comps/0607/recommend/recommender/svd.html
%%%%% - IMPORTANT NOTE:
%%%%% - whichever rows you eliminate from recom_matrix you MUST also remove from
%%%%% - Y_mean since later we row-wise add the these matrices.
%%%%% - More Notes:
%%%%% - Going based on this: http://infolab.stanford.edu/~ullman/mmds/ch11.pdf

recom_svd = recom_matrix;
Y_svd = Y_mean;

m = size(recom_matrix, 2);

%% mean normalization
rm_mean = mean(recom_matrix);
rm_std = std(recom_matrix);
rm_norm = recom_matrix;

for i = 1:m
    rm_norm(:, i) = (recom_matrix(:, i) - rm_mean(i)) / rm_std(i);
endfor

%% using cov to calculate covariance matrix
cov_mat = (rm_norm' * rm_norm) / m;

%% svd of covariance matrix
[U, S, V] = svd(cov_mat);

%% Take 90% of the dimensions
new_U = U(:, 1:uint32(size(U, 1) * 0.90));

%% Apply reduction:
recom_matrix = recom_matrix * new_U;

end
