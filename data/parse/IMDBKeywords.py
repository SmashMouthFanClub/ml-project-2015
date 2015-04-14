import re
import progbar
from util import *

# for finding the section headers in the keywords.list.# files
sectionRegex = re.compile('^(\d)\:')

# splits a tag and its count in the tag summary section
tagCountRegex = re.compile('(.+) \((\d+)')

def parseIMDBKeywords(movieID, movieTitle, movieTags, tagID, tagCount, files):
  lines = batchOpen(files, encoding = 'iso-8859-1')
  totalLines = lineCount(files)
  lineNum = 0
  progBar = progbar.ProgressBar(totalLines)

  # first, get to the summary of all of the different keywords
  for line in lines:
    lineNum += 1
    match = sectionRegex.match(line)
    if match != None and match.group(1) == '4':
      break

  progBar.update(lineNum)

  # next, read in all of the tag counts
  for line in lines:
    lineNum += 1
    match = sectionRegex.match(line)
    if match != None and match.group(1) == '5':
      break
    newTags = getTagCounts(line)
    tagCount.extend(newTags)

  progBar.update(lineNum)

  # then, skip to the start of the movie-tag pairs
  for line in lines:
    lineNum += 1
    match = sectionRegex.match(line)
    if match != None and match.group(1) == '8':
      break

  progBar.update(lineNum)

  # finally, parse the movies until end of file
  for line in lines:
    lineNum += 1
    if lineNum % 5000 == 0:
      progBar.update(lineNum)
    (title, tag) = getMovieTag(line)
    if tag == None or not isMovie(title):
      continue
    cleanTitle = scrub(title)
    if cleanTitle in movieID:
      idx = movieID[cleanTitle]
      movieTags[idx].append(tag)
    else:
      movieID[cleanTitle] = len(movieTags)
      movieTags.append([tag])
      movieTitle.append(title)

  stats = {
    'tag-count': len(tagCount),
    'movie-count': len(movieTitle)
  }

  return stats

def getTagCounts(line):
  outTags = []
  tags = line.split(')')
  for tag in tags:
    match = tagCountRegex.match(tag.strip())
    if match != None:
      outTags.append((match.group(1), int(match.group(2))))
  return outTags

def getMovieTag(line):
  movieTag = [x.strip() for x in line.split('\t') if x.strip() != '']
  if len(movieTag) != 2:
    return (None, None)
  else:
    return(movieTag[0], movieTag[1])
