%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% svdReduce.m
% This file will use SVD to reduce the dimensionality of the movie
% recommendation matrix.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [recom_svd, U_reduce] = svdReduce(recom_matrix)
	 
  %%%%% TODO - Misael
  %%%%% - use svd to reduce the dimensionality of the recommendation matrix
  %%%%% - passed into the function.  For now, I just return the matrix.
  %%%%% - For a good source, see:
  %%%%% - http://www.cs.carleton.edu/cs_comps/0607/recommend/recommender/svd.html
  %%%%% - IMPORTANT NOTE:
  %%%%% - whichever rows you eliminate from recom_matrix you MUST also remove from
  %%%%% - Y_mean since later we row-wise add the these matrices.
  %%%%% - More Notes:
  %%%%% - Going based on this: http://www.cs.otago.ac.nz/cosc453/student_tutorials/principal_components.pdf
	 
  recom_svd = recom_matrix;
  
  m = size(recom_matrix, 1);
  
  %% mean normalization
  rm_mean = mean(recom_matrix);
  rm_std = std(recom_matrix);
  rm_norm = recom_matrix;
  
  rm_norm = bsxfun(@minus, recom_matrix, rm_mean);
  rm_norm = bsxfun(@rdivide, rm_norm, rm_std);
  
  %% calculate covariance matrix
  cov_mat = cov(recom_matrix);

  %% svd of covariance matrix
  [U, S, V] = svd(cov_mat);
  
  %% Choosing k based on 0.99 variance retained
  %% From Andrew Ng video on "Choosing the Number of Principal Components"
  k = size(S, 1);
  sums = sum(diag(S));
  sumk = 0;
  
  for i = 1:size(S, 1)
    if (sumk / sums < 0.99)
      sumk = sumk + S(i, i);
    else
      k = i;
      break;
    endif
  endfor
  
  printf("Reducing from %d to %d dimensions\n", size(recom_matrix, 2), k);
  
  %% Take 90% of the dimensions
  U_reduce = U(:, 1:k);
  
  %% Apply reduction:
  recom_matrix = recom_matrix * U_reduce;
  
  %% Undo mean normalization:
  for i = 1:k
    recom_matrix(:, i) = (recom_matrix(:, i) * rm_std(i)) + rm_mean(i);
  endfor
  
  recom_svd = recom_matrix;
end
