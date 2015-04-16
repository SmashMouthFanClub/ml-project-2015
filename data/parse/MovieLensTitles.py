import json
import progbar
import re
from util import *

movieLensTitle = re.compile('^(\d+)::(.*?) \(.*?(\d+)\)::.*$')

lensArticleRegex = re.compile('^(.*?), ?(The|A|An|Los|Les|La|Le|El|L\')$')

def parseMovieLensTitles(movieID, movieTitle, lensID, files, matchFile):
  lines = batchOpen(files)
  fMatch = open(matchFile, 'r')
  cachedMatches = json.load(fMatch)
  fMatch.close()

  totalLines = lineCount(files)
  lineNum = 0
  progBar = progbar.ProgressBar(totalLines)

  parseErr = 0
  missed = 0
  matched = 0

  for line in lines:
    match = movieLensTitle.match(line)
    if match == None:
      print(line)
      parseErr += 1
      continue
    
    idx = int(match.group(1))
    dirtyTitle = fixArticle(match.group(2)) + ' (' + match.group(3) + ')'
    cleanTitle = scrub(dirtyTitle)
    
    if cleanTitle in movieID:
      idxIMDB = list(set(movieID[cleanTitle]))
      if len(idxIMDB) != 1 and dirtyTitle in cachedMatches:
        if str(cachedMatches[dirtyTitle]).isdigit():
          idxOld = cachedMatches[dirtyTitle]
          cachedMatches[dirtyTitle] = movieTitle[idxOld]
        idxIMDB = cachedMatches[dirtyTitle]
      elif len(idxIMDB) != 1:
        x = [movieTitle[i] for i in idxIMDB]
        if dirtyTitle in x:
          idxIMDB = idxIMDB[x.index(dirtyTitle)]
        else:
          idxIMDB = chooseTitle(movieTitle, idxIMDB, dirtyTitle)
        cachedMatches[dirtyTitle] = movieTitle[idxIMDB]
      else:
        idxIMDB = idxIMDB[0]

      matched += 1
    else:
      lensID.append(cleanTitle)
      missed += 1

  prettyPrint(cachedMatches, matchFile)

  return {
    'parseErr': parseErr,
    'missed': missed,
    'matched': matched
  }

def fixArticle(title):
  match = lensArticleRegex.match(title)
  if match == None:
    return title
  else:
    return match.group(2) + ' ' + match.group(1)

def chooseTitle(movieTitle, choices, title):
  print('Which is the correct matching for {}?'.format(title))
  for idx, x in enumerate(choices):
    print('\t{}:\t{}'.format(idx + 1, movieTitle[x]))
  matchIdx = int(input())
  return choices[(matchIdx - 1) % len(choices)]
