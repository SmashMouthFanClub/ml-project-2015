from operator import itemgetter
import itertools
import re
import string

# files to produce:
#   tags.txt:    tag id :: tag name :: occurences
#   movies.txt:  movie id :: movie name :: tag id #1, tag id #2, ....
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

################################################################################
# 
################################################################################

def listMovies(movies, files):
  files = batchOpen(files)
  for line in files:
    title = getMovieTitle(line)
    if title != None:
      movies[title] = []

def listTags(movies, tags, files):
  files = batchOpen(files)
  state = 0
  
  for line in files:
    if state == 4:
      regex = re.compile('^(5)\:')
      match = regex.match(line)
      if match == None:
        tags.extend(getTagCounts(line))
      else:
        state = int(match.group(1))
    elif state == 8:
      movieTag = getMovieTag(line)
      if movieTag != None and movieTag[0] in movies:
        movies[movieTag[0]].append(movieTag[1])
    else:
      regex = re.compile('^(\d)\:')
      match = regex.match(line)
      if match != None:
        state = int(match.group(1))

  sorted(tags, key = itemgetter(1))

def listGenresAsTags(movies, tags, files):
  files = batchOpen(files)
  state = 0

  for line in files:
    if state == 3:
      regex = re.compile('^(4)\:')
      match = regex.match(line)
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
      regex = re.compile('^(\d)\:')
      match = regex.match(line)
      if match != None:
        state = int(match.group(1))

def pruneOrphanMovies(movies, minTags):
  orphanList = []
  for movie in movies.keys():
    tags = movies[movie]
    if len(tags) <= minTags:
      orphanList.append(movie)
  stats = (len(orphanList), len(movies), len(orphanList) / len(movies))
  for orphan in orphanList:
    movies.pop(orphan)
  return stats

def substitueTags(movies, tags):
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
  regex = re.compile('^((?:\".*?\")|(?:.*?)) \(.*$')
  match = regex.match(line)
  if match == None:
    return None
  else:
    return match.group(1).strip('"')

def getTagCounts(line):
  outTags = []
  tags = line.split(')')
  regex = re.compile('(.+) \((\d+)')
  for tag in tags:
    match = regex.match(tag.strip())
    if match != None:
      outTags.append((match.group(1), int(match.group(2))))
  return outTags

def getMovieTag(line):
  regex = re.compile('^((?:\".*?\")|(?:.*?)) \(.*\t+(.*)$')
  match = regex.match(line)
  if match == None:
    return None
  else:
    return (match.group(1).strip('"'), match.group(2).strip().lower())

def getGenreCount(line):
  regex = re.compile('^(.+?)[\t ]+(\d+)$')
  match = regex.match(line)
  if match == None:
    return None
  else:
    return (match.group(1).strip().lower(), int(match.group(2)))

if __name__ == '__main__':
  movies = {}
  tags = []

  listMovies(movies, movieFiles)
  listTags(movies, tags, tagFiles)
  listGenresAsTags(movies, tags, genreFiles)

  pruneOrphanMovies(movies, 1))

  substituteTags(movies, tags)
