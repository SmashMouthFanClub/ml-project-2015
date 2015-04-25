%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 91.427/545 Machine Learning
% Mike Stowell, Anthony Salani, Misael Moscat
%
% Main Driver
% Loads the text file that maps movie IDs to their respective titles
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function id_map = loadMovieIDNameMap(file_name)

% read the file
fid = fopen(file_name);

% initialize the cell array of IDs to names and a counting index
id_map = cell(1,1);
i = 0;

while(!feof(fid))
  % increment index and read line
  i = i + 1;
  line = fgets(fid);

  %%%%% TODO - can get rid of this part once we have our own movie title data
  % ignore any proceeding ID number by splitting on a space
  %[idx, movie_name] = strtok(line, ' ');

  % add the movie name to the array
  id_map{i} = strtrim(line); % strtrim(movie_name);
endwhile

% close the file
fclose(fid);

end
