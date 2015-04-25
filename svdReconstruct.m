%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% svdReconstruct.m
% This file will reconstruct an approximate movie recommendation matrix
% from the SVD reduced movie recommendation matrix
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function recom_matrix = svdReconstruct(recom_svd, U_reduce)
  recom_matrix = recom_svd * U_reduce';
end
