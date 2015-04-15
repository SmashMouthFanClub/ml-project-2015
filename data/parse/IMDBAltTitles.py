import re
import progbar
from util import *

akaTitle = re.compile('^ +\(aka (\".*\"|.*) ((?:\(\d+\))|(?:\(\?+\))).*$')

def parseIMDBAltTitles(movieID, files):
  lines = batchOpen(files, encoding = 'iso-8859-1')
  
  totalLines = lineCount(files)
  lineNum = 0
  progBar = progbar.ProgressBar(totalLines)

  missed = 0
  matched = 0
  altTitles = 0
  currTitleID = None

  for line in lines:
    lineNum += 1
    if lineNum % 5000 == 0:
      progBar.update(lineNum)

    if lineNum < 17:
      continue

    if line[0] == ' ':
      match = akaTitle.match(line)
      if match == None:
        continue

      cleanTitle = scrub(match.group(1).strip('"') + ' ' + match.group(2))

      if currTitleID != None and cleanTitle not in movieID:
        altTitles += 1
        movieID[cleanTitle] = [currTitleID]
      elif currTitleID != None:
        altTitles += 1
        movieID[cleanTitle].append(currTitleID)
    elif isMovie(line):
      cleanTitle = scrub(line)

      if cleanTitle in movieID:
        matched += 1
        currTitleID = movieID[cleanTitle][0]
      else:
        missed += 1
        currTitleID = None

  return {
    'missed': missed,
    'matched': matched,
    'altTitles': altTitles
  }
