from operator import itemgetter
import itertools
import re
import string

# files to produce:
#   tags.txt:    tag id :: tag name :: # occurences
#   movies.txt:  movie id :: movie name :: # ratings :: tag ids
#   ratings.txt: user id :: movie id :: rating
#
#   given a user's list of movie ratings, find those movies in the movies.txt
#    file.  take each tag, and average the scores of the movies with each tag.
#    this creates the user's ratings of individual tags - gaps should be an
#    average value (0, 2.5, etc...).
#   then, construct the .mat file using the above method for every other user

movieFiles = [
  'raw/movies.list.0',
  'raw/movies.list.1',
  'raw/movies.list.2'
]

tagFiles = [
  'raw/keywords.list.0',
  'raw/keywords.list.1',
  'raw/keywords.list.2',
  'raw/keywords.list.3',
  'raw/keywords.list.4'
]

genreFiles = [
  'raw/genres.list.0',
  'raw/genres.list.1'
]

lensFiles = [
  'raw/movies.dat.0'
]

ratingFiles = [
  'raw/ratings.dat.0',
  'raw/ratings.dat.1',
  'raw/ratings.dat.2',
  'raw/ratings.dat.3',
  'raw/ratings.dat.4',
  'raw/ratings.dat.5'
]

sectionRegex = re.compile('^(\d)\:')
line4Regex = re.compile('^(4)\:')
line5Regex = re.compile('^(5)\:')
movieTitleRegex = re.compile('^((?:\".*?\")|(?:.*?)) \(.*$')
tagCountRegex = re.compile('(.+) \((\d+)')
movieTagRegex = re.compile('^((?:\".*?\")|(?:.*?)) \(.*\t+(.*)$')
genreCountRegex = re.compile('^(.+?)[\t ]+(\d+)$')
lensRegex = re.compile('^(\d+)::(.*?) \(.*?::.*$')
lensArticleRegex = re.compile('^(.*?), ?(The|A|An|Los|Les)$')


################################################################################
# 
################################################################################

def listMovies(movies, movieTags, movieRatings, files):
  files = batchOpen(files)
  for line in files:
    title = getMovieTitle(line)
    if title != None:
      movies.append(title)
      movieTags[title] = []
      movieRatings[title] = 0

def listTags(movies, tags, files):
  files = batchOpen(files)
  state = 0
  
  for line in files:
    if state == 4:
      match = line5Regex.match(line)
      if match == None:
        tags.extend(getTagCounts(line))
      else:
        state = int(match.group(1))
    elif state == 8:
      movieTag = getMovieTag(line)
      if movieTag != None and movieTag[0] in movies:
        movies[movieTag[0]].append(movieTag[1])
    else:
      match = sectionRegex.match(line)
      if match != None:
        state = int(match.group(1))

  sorted(tags, key = itemgetter(1))

def listGenresAsTags(movies, tags, files):
  files = batchOpen(files)
  state = 0

  for line in files:
    if state == 3:
      match = line4Regex.match(line)
      if match == None:
        genre = getGenreCount(line)
        if genre != None:
          tags.append(genre)
      else:
        state = int(match.group(1))
    elif state == 8:
      genreTag = getMovieTag(line)
      if genreTag != None and genreTag[0] in movies:
        movies[genreTag[0]].append(genreTag[1])
    else:
      match = sectionRegex.match(line)
      if match != None:
        state = int(match.group(1))

def listMovieRatings(movies, files):
  files = batchOpen(files)
  good = 0
  bad = 0

  lensIDs = {}

  for line in files:
    movie = getLensMovie(line)
    if movie[1] in movies:
      lensIDs[movie[1]] = movie[0]
      good += 1
    else:
      print(movie[1])
      bad += 1

def pruneOrphanMovies(movies, movieTags, minTags):
  orphanList = []
  for movie in movies.keys():
    tags = movies[movie]
    if len(tags) <= minTags:
      orphanList.append(movie)
  stats = (len(orphanList), len(movies), len(orphanList) / len(movies))
  for orphan in orphanList:
    movies.pop(orphan)
  return stats

def enumerateMovies(movies, movieIDs):
  for idx, movie in enumerate(movies):
    movieIDs[movie] = str(idx)

def enumerateTags(tags, tagIDs):
  for idx, tag in enumerate(tags):
    tagIDs[tag[0]] = str(idx)

def serializeMovies(movies, tags, tagIDs, outFile):
  for idx, key in enumerate(movies.keys()):
    movieTagIDs = ','.join([tagIDs[tag] for tag in movies[key]])
    print('{}::{}::{}'.format(idx, key, movieTagIDs))

def serializeTags(movies, tags, tagIDs, outFile):
  1

################################################################################
# Opens a bunch of files at once for reading                                   #
################################################################################

def batchOpen(files):
  files = [open(f, 'r', errors = 'replace') for f in files]
  return itertools.chain.from_iterable(files)

################################################################################
# Functions for extracting information from various file formats               #
################################################################################

def getMovieTitle(line):
  match = movieTitleRegex.match(line)
  if match == None:
    return None
  else:
    return match.group(1).strip('"')

def getTagCounts(line):
  outTags = []
  tags = line.split(')')
  for tag in tags:
    match = tagCountRegex.match(tag.strip())
    if match != None:
      outTags.append((match.group(1), int(match.group(2))))
  return outTags

def getMovieTag(line):
  match = movieTagRegex.match(line)
  if match == None:
    return None
  else:
    return (match.group(1).strip('"'), match.group(2).strip().lower())

def getGenreCount(line):
  match = genreCountRegex.match(line)
  if match == None:
    return None
  else:
    return (match.group(1).strip().lower(), int(match.group(2)))

def getLensMovie(line):
  match = lensRegex.match(line)
  if match == None:
    return None
  else:
    movieTitle = match.group(2).strip()
    theMatch = lensArticleRegex.match(movieTitle)
    if theMatch == None:
      return (match.group(1), movieTitle)
    else:
      return (match.group(1), theMatch.group(2) + ' ' + theMatch.group(1))

if __name__ == '__main__':
  movies = []
  movieIDs = {}
  movieTags = {}
  movieRatings = {}

  tags = []
  tagIDs = {}

  listMovies(movies, movieTags, movieRatings, movieFiles)
  enumerateMovies(movies, movieIDs)

  listTags(movieTags, tags, tagFiles)
  listGenresAsTags(movieTags, tags, genreFiles)
  pruneOrphanMovies(movies, movieTags, 1)
  enumerateTags(tags, tagIDs)

  #listMovieRatings(movies, lensFiles)
  


  #serializeMovies(movies, tags, tagIDs, 'parsed.movies.txt')
  #serializeTags(movies, tags, tagIDs, 'parsed.tags.txt')
