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

recom_svd = recom_matrix;
Y_svd = Y_mean;

[U, S, V] = svd(recom_matrix, 1);

D = diag(S);
energy = sum(D .^ 2);

for i = 1:(size(D, 1) / 2)
    [val index] = min(D);

    D(index) = Inf;
    S(index, :) = 0;
endfor

D = diag(S);
energy2  = sum(D .^ 2);

energy2 / energy

end
