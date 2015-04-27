import argparse
from operator import attrgetter, itemgetter
import re
from util import *

inMovies = ['tmp/movies.txt']
inTags = ['tmp/tags.txt']
inUsers = ['tmp/users.txt']

outMatrix = 'movies.mat'
outTitles = 'titles.txt'

moviesRegex = re.compile('^(\d+)::(.+)::([0-9,]+)$')
tagsRegex = re.compile('^(\d+)::(.+)::(\d+)$')
usersRegex = re.compile('^(\d+)::([0-9,]+)::([0-9.,]+)$')

def loadMovies(movies, files):
  lines = batchOpen(files)
  for line in lines:
    match = moviesRegex.match(line)
    movies.append({
      'id': int(match.group(1)),
      'name': match.group(2),
      'tags': [int(x) for x in match.group(3).split(',')]
      })

def loadTags(tags, files):
  lines = batchOpen(files)
  for line in lines:
    match = tagsRegex.match(line)
    tags.append({
      'id': int(match.group(1)),
      'name': match.group(2),
      'count': int(match.group(3))
      })

def loadUsers(users, files):
  lines = batchOpen(files)
  for line in lines:
    match = usersRegex.match(line)
    movieIDs = [int(x) for x in match.group(2).split(',')] 
    ratings = [float(x) for x in match.group(3).split(',')]
    users.append({
      'id': int(match.group(1)),
      'ratings': list(zip(movieIDs, ratings))
      })

def convertToTagRatings(movies, tags, users):
  for user in users:
    totals = {}
    for movieIdx, rating in user['ratings']:
      for idx in movies[movieIdx]['tags']:
        if idx in totals:
          total, count = totals[idx]
          totals[idx] = (total + rating, count + 1)
        else:
          totals[idx] = (rating, 1)
    user['ratings'] = [(idx, totals[idx][0] / totals[idx][1]) for idx in totals.keys()]
    print(user['id'])

def filterTagsByCount(movies, tags, users, minHits):
  oldTagCount = len(tags)
  tags[:] = [tag for tag in tags if tag['count'] > minHits]

  tagMap = {}
  reIndex(tags, tagMap)

  removedTagInstances = 0
  for movie in movies:
    oldMovieTags = len(movie['tags'])
    movie['tags'] = [tagMap[idx] for idx in movie['tags'] if idx in tagMap]
    removedTagInstances += oldMovieTags - len(movie['tags'])

  return {
    'removedTags': oldTagCount - len(tags),
    'removedTagInstances': removedTagInstances
  }

def filterTaglessMovies(movies, tags, users):
  movies[:] = [movie for movie in movies if len(movie['tags']) != 0]
  movieMap = {}
  reIndex(movies, movieMap)

def filterMoviesByRatings(movies, users):
  ratedMovies = set()
  for user in users:
    for idx, _ in user['ratings']:
      ratedMovies.add(idx)

  movies[:] = [x for x in movies if x['id'] in ratedMovies]
  movieMap = {}
  reIndex(movies, movieMap)

  for user in users:
    user['ratings'] = [(movieMap[idx], rating) for idx, rating in user['ratings']]

  return {
    'numUsers': len(users),
    'numMovies': len(ratedMovies)
  }

def outputMovieTagsMatrix(movies, numRows, numCols, fileName):
  f = open(fileName, 'w')
  print('# name: Z', file = f)
  print('# type: matrix', file = f)
  print('# rows: {}'.format(numRows), file = f)
  print('# columns: {}'.format(numCols), file = f)
  for movie in movies:
    tagList = ['0'] * numCols
    for idx in movie['tags']:
      tagList[idx] = '1'
    print(' '.join(tagList), file = f)

def outputRatingsMatrix(users, numRows, numCols, fileName):
  f = open(fileName, 'w')
  print('# name: Y', file = f)
  print('# type: matrix', file = f)
  print('# rows: {}'.format(numRows), file = f)
  print('# columns: {}'.format(numCols), file = f)
  for user in users:
    ratingList = ['0'] * numCols
    for idx, rating in user['ratings']:
      ratingList[idx] = str(rating)
    print(' '.join(ratingList), file = f)

def outputMoviesLookup(movies, fileName):
  f = open(fileName, 'w')
  for movie in movies:
    print(movie['name'], file = f)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(dest = 'output')
  subparsers.required = True
  parserTags = subparsers.add_parser('tags')
  parserTags.add_argument('-c', '--count', default = 1400, type = int)
  parserMovies = subparsers.add_parser('movies')
  args = parser.parse_args()

  movies = []
  tags = []
  users = []
  if args.output == 'tags':
    loadMovies(movies, inMovies)
    loadTags(tags, inTags)
    loadUsers(users, inUsers)
    filterTagsByCount(movies, tags, users, args.count)
    convertToTagRatings(movies, tags, users)
    filterTaglessMovies(movies, tags, users)
    outputRatingsMatrix(users, len(users), len(tags), 'recommend.mat')
    outputMovieTagsMatrix(movies, len(movies), len(tags), 'movietags.mat')
    outputMoviesLookup(movies, 'movies.lookup')
  elif args.output == 'movies':
    loadMovies(movies, inMovies)
    loadUsers(users, inUsers)
    stats = filterMoviesByRatings(movies, users)
    outputRatingsMatrix(users, len(users), len(movies), 'recommend.mat')
    outputMoviesLookup(movies, 'movies.lookup')
