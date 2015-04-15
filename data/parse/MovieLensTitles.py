import re
import progbar
from util import *

movieLensTitle = re.compile('^(\d+)::(.*?) \(.*?(\d+).*$')

def parseMovieLensTitles(files):
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
      parseErr += 1

    idx = int(match.group(1))
    title = scrub(match.group(2) + ' (' + match.group(3) + ')')

