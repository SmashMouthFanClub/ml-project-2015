import re
import progbar
from util import *

# for finding the section headers in the keywords.list.# files
sectionNumber = re.compile('^(\d)\:')

# splits a tag and its count in the tag summary section
genreCount = re.compile('(.+?) +(\d+)$')

def parseIMDBGenres(movieID, movieTitle, movieTags, tagID, tagCount, files):
  lines = batchOpen(files, encoding = 'iso-8859-1')
  totalLines = lineCount(files)
  lineNum = 0
  progBar = progbar.ProgressBar(totalLines)

  # first, get to the summary of all of the different keywords
  for line in lines:
    lineNum += 1
    match = sectionNumber.match(line)
    if match != None and match.group(1) == '3':
      break

  progBar.update(lineNum)

  # next, read in all of the tag counts
  for line in lines:
    lineNum += 1
    match = sectionNumber.match(line)
    if match != None and match.group(1) == '4':
      break
    newTag = getGenreCount(line)
    tagCount.extend(newTag)

  progBar.update(lineNum)

  # then, skip to the start of the movie-tag pairs
  for line in lines:
    lineNum += 1
    match = sectionNumber.match(line)
    if match != None and match.group(1) == '8':
      break

  progBar.update(lineNum)

  # finally, parse the movies until end of file
  skipped = 0
  added = 0
  for line in lines:
    lineNum += 1
    if lineNum % 5000 == 0:
      progBar.update(lineNum)
    (title, genre) = getMovieGenre(line)
    if genre == None or not isMovie(title):
      continue
    cleanTitle = scrub(title)
    if cleanTitle in movieID:
      added += 1
      idx = movieID[cleanTitle][0]
      movieTags[idx].append(genre)
    else:
      skipped += 1

  stats = {
    'tag-count': len(tagCount),
    'movie-count': len(movieTitle),
    'skipped': skipped,
    'added': added
  }

  return stats

def getGenreCount(line):
  outTags = []
  match = genreCount.match(line)
  if match == None:
    return []
  else:
    return [(match.group(1).lower().strip(), int(match.group(2)))]

def getMovieGenre(line):
  movieTag = [x.strip() for x in line.split('\t') if x.strip() != '']
  if len(movieTag) != 2:
    return (None, None)
  else:
    return(movieTag[0], movieTag[1].lower())
