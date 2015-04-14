import re
import progbar
from util import *

def parseIMDBAltTitles(movieID, files):
  lines = batchOpen(files, encoding = 'iso-8859-1')
  #totalLines = lineCount(files)
  lineNum = 0
  #progBar = progbar.ProgressBar(totalLines)

  missed = 0
  matched = 0
  other = 0

  for line in lines:
    lineNum += 1
    #if lineNum % 5000 == 0:
    #  progBar.update(lineNum)

    if lineNum < 17:
      continue

    currTitleID = None
    if line[0] == ' ':
      other += 1
      if currTitleID != None:
        continue
    elif isMovie(line):
      cleanTitle = scrub(line)
      print(cleanTitle)
      if cleanTitle in movieID:
        matched += 1
        currTitleID = movieID[cleanTitle]
      else:
        missed += 1
        currTitleID = None


  return {
    'missed': missed,
    'matched': matched,
    'other': other
  }
