Q = require('q');
yargs = require('yargs');
lineReader = require('line-reader');

/*

THINGS TO DO:

* create table of movies
* create table that maps MovieLens movie IDs to IMDB IDs
* run through movies, split it into equally sized lists based on # of ratings
* run through tags, split it into equally sized lists based on # of occurences

*/

loadMovies = function() {
  var isTitle = /\"?(.+?)\"? \(.*$/;
  var titles = {};
  var files = [
    'raw/movies.list.0',
    'raw/movies.list.1',
    'raw/movies.list.2'
  ];

  for (file in files) {
    var deferred = Q.defer();

    lineReader.eachLine(file, function(line, last) {
      var result = isTitle.exec(line);
      if (result != null && !(result[1] in titles)) {
        titles[result[1]] = 0;
      }
    }).then(function() {
      deferred.resolve(null);
    });

    deferred.promise.done();
  }

  console.log('done!');
};

loadMovies();
