import re
import progbar
from util import *

movieLensTitle = re.compile('^(\d+)::(.*?) \(.*?(\d+)\)::.*$')

lensArticleRegex = re.compile('^(.*?), ?(The|A|An|Los|Les|La|Le|El|L\')$')

def parseMovieLensTitles(movieID, lensID, files):
  lines = batchOpen(files)

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
    title = scrub(fixArticle(match.group(2)) + ' (' + match.group(3) + ')')
    
    if title in movieID:
      idxIMDB = list(set(movieID[title]))
      if len(idxIMDB) != 1:
        idxIMDB = dict(enumerate(idxIMDB))
        print(idxIMDB)
      else:
        1
        #lensID[idx] = idxIMDB[0]
      matched += 1
    else:
      lensID.append(title)
      missed += 1

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
