from operator import itemgetter
import codecs
import itertools
import re
import string

################################################################################
# files to produce:                                                            #
#   tags.txt:    tag id :: tag name :: # occurences                            #
#   movies.txt:  movie id :: movie name :: # ratings :: tag ids                #
#   ratings.txt: user id :: movie id :: rating                                 #
#                                                                              #
#   given a user's list of movie ratings, find those movies in the movies.txt  #
#    file.  take each tag, and average the scores of the movies with each tag. #
#    this creates the user's ratings of individual tags - gaps should be an    #
#    average value (0, 2.5, etc...).                                           #
#   then, construct the .mat file using the above method for every other user  #
################################################################################

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
lensArticleRegex = re.compile('^(.*?), ?(The|A|An|Los|Les|La|Le|El|L\')$')
romanNumerals


################################################################################
# Parsing functions.  Because every set of files is entirely different in how  #
#   they are structured, each file gets its own function with a vastly         #
#   different function signature.  By far the most expensive part is here.     #
################################################################################

def listMovies(movies, movieTags, movieRatings, files):
  files = batchOpen(files, encoding = 'iso-8859-1')
  for line in files:
    title = getMovieTitle(line)
    if title != None and title not in movieTags:
      movies.append(title)
      movieTags[title] = []
      movieRatings[title] = 0

def listTags(movies, tags, files):
  files = batchOpen(files, encoding = 'iso-8859-1')
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
  files = batchOpen(files, encoding = 'iso-8859-1')
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

def listMovieRatings(movies, movieRatings, files):
  files = batchOpen(files)
  good = 0
  bad = 0
  err = 0

  lensIDs = {}

  for line in files:
    movie = getLensMovie(line)
    if movie != None and movie[1] in movieRatings:
      lensIDs[movie[1]] = movie[0]
      good += 1
    elif movie != None:
      print(movie[1])
      bad += 1
    else:
      print('ERR:', line)
      err += 1

  print(good, bad, err)

################################################################################
# Pruning movies/tags/ratings that have no associated movies/tags/ratings      #
# Probably will move this functionality to the other file.  Already performing #
#   minimal pruning during the parse step (ex: ignoring tags for movies not in #
#   the database, ignoring ratings for movies not in the database).  A more    #
#   comprehensive pruning should be done when generating specific datasets to  #
#   guarantee no data is permanently lost.                                     #
################################################################################

def pruneOrphanMovies(movies, movieTags, minTags):
  moviesList = []
  orphanList = []
  for movie in movies:
    tags = movieTags[movie]
    (moviesList if len(tags) > minTags else orphanList).append(movie)
  stats = (len(orphanList), len(moviesList), len(orphanList) / len(movies))
  for orphan in orphanList:
    movieTags.pop(orphan)
  movies[:] = moviesList
  return stats

################################################################################
# Enumeration allows for a smaller file size.  Instead of repeating "Godzilla  #
#   vs. Mechagodzilla" or "wwii-post-war-drama", it will repeat smaller        #
#   numbers like "54060" and "675393".  This is a guaranteed win as long as    #
#   the movie or tag title is more than six characters, which is the vast      #
#   majority of them.                                                          #
################################################################################

def enumerateMovies(movies, movieIDs):
  for idx, movie in enumerate(movies):
    movieIDs[movie] = str(idx)

def enumerateTags(tags, tagIDs):
  for idx, tag in enumerate(tags):
    tagIDs[tag[0]] = str(idx)

################################################################################
# Serialization just takes each list of movies/tags/ratings and outputs a file #
#   that is sane and requires very little work to extract data from.           #
################################################################################

def serializeMovies(movies, tags, tagIDs, outFile):
  for idx, key in enumerate(movies.keys()):
    movieTagIDs = ','.join([tagIDs[tag] for tag in movies[key]])
    #print('{}::{}::{}'.format(idx, key, movieTagIDs))

def serializeTags(movies, tags, tagIDs, outFile):
  1

################################################################################
# Opens a bunch of files at once for reading.                                  #
################################################################################

def batchOpen(files, encoding=None):
  if encoding == None:
    files = [open(f, 'r') for f in files]
  else:
    files = [codecs.open(f, 'r', encoding) for f in files]
  return itertools.chain.from_iterable(files)

################################################################################
# Functions for extracting information from various file formats.              #
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

################################################################################
# Takes a movie title and permutes a bunch of possible alternate titles
################################################################################

def permuteTitles(title):

################################################################################
# Converts a given title to a simplified version.  Simplified titles are       #
# lacking capitalization, spaces, punctuation, etc...                          #
# Numberes are also converted to Roman numerals.                               #
################################################################################

def simplifyTitle(title):


################################################################################
# Main driver.                                                                 #
################################################################################

if __name__ == '__main__':
  movies = []
  movieIDs = {}
  movieTags = {}
  movieRatings = {}

  tags = []
  tagIDs = {}

  listMovies(movies, movieTags, movieRatings, movieFiles)
  listTags(movieTags, tags, tagFiles)
  listGenresAsTags(movieTags, tags, genreFiles)
  listMovieRatings(movies, movieRatings, lensFiles)

  #pruneOrphanMovies(movies, movieTags, 1)
  #pruneOrphanTags()

  #enumerateMovies(movies, movieIDs)
  #enumerateTags(tags, tagIDs)

  #serializeMovies(movies, tags, tagIDs, 'parsed.movies.txt')
  #serializeTags(movies, tags, tagIDs, 'parsed.tags.txt')

