%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% genTestSet.m
% Split the data into training and test set, applying p percent of the
% data to the test set. Then extract away q percent of the test values.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [Y, Y_test] = genTestSet(Y, p, q)

% split the first p percent rows into a test set
[m, n] = size(Y);
col_idx = floor(p * n);
Y_test = Y(:, 1:col_idx);

% randomly remove q percent of ratings from the test set
for i = 1 : col_idx

    % get the user
    user = Y_test(:, i);

    % find the amount of ratings by this user
    num_ratings = sum(user > 0);

    % determine the amount of ratings to remove
    rem = floor(num_ratings * q);

    % remove the first rem ratings
    for j = 1 : length(user)
        if (rem <= 0)
           break;
        end
        if (user(j) > 0)
           Y(j, i) = 0;
           rem = rem - 1;
        end
    end
end

end
