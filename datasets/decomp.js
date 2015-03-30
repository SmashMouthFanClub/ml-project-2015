/*
  Downloads the required datasets.  This should only need to be run once.
*/

var fs = require('fs');

var files = [
  {
    name: 'MovieLens 10M/100K',
    path: 'tmp/movielens.zip',
    url: 'http://files.grouplens.org/datasets/movielens/ml-10m.zip'
  },
  {
    name: 'IMDB Keywords',
    path: 'tmp/imdb.keywords.gz',
    url: 'ftp://ftp.fu-berlin.de/pub/misc/movies/database/keywords.list.gz'
  },
  {
    name: 'Test',
    path: 'big/game/long/name/asdf.poop',
    url: 'dada'
  },
  {
    name: 'Test',
    path: 'asdf.poop',
    url: 'dada'
  }
];

var createDirectories = function(path) {
  var splitPath = path.split('/');
  splitPath.slice(0, splitPath.length - 1).forEach(function(directory, i) {
    try {
      fs.mkdirSync(splitPath.slice(0, i + 1).join('/'));
    } catch (e) {
      if (e.code !== 'EEXIST') throw e;
    }
  });
};

files.forEach(function(file, i) {
  // create directory for file
  createDirectories(file.path);

  // download file

  // extract file
});
