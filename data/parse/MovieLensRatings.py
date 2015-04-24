import re
import progbar
from util import *

ratingsRegex = re.compile('^(\d+)::(\d+)::((?:[0-5]\.\d)|(?:[1-5])).*$')

def parseMovieLensRatings(lensID, userRatings, files):
  lines = batchOpen(files)
  totalLines = lineCount(files)
  lineNum = 0
  progBar = progbar.ProgressBar(totalLines)

  parseErr = 0
  unmatched = set()

  lastUser = None

  for line in lines:
    lineNum += 1
    if lineNum % 5000 == 0:
      progBar.update(lineNum)

    match = ratingsRegex.match(line)
    if match == None:
      print(line)
      parseErr += 1
      continue

    userID = match.group(1)
    movieID = int(match.group(2))
    rating = float(match.group(3))

    if movieID in lensID:
      movieID = lensID[movieID]
    else:
      unmatched.add(movieID)
      continue

    if userID == lastUser:
      userRatings[-1].append((movieID, rating))
    else:
      lastUser = userID
      userRatings.append([(movieID, rating)])

  return {
    'unmatched': len(unmatched),
    'parseErr': parseErr
  }
