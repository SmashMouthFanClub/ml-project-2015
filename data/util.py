import codecs
import itertools
import json
import re
import subprocess
import unicodedata as ud

fileCountTotal = re.compile('.* (\d+).*', re.M | re.S)

unicodeDel = re.compile('(?:[,.\'"?!]|[^\x00-\x7f])+')

unicodeSub = re.compile('(?:[\s\-/\ :()[\]{}])+')

andSub = re.compile('\&')

isNumber = re.compile('\d+')

endingDel = re.compile('\-(?:v|vg|tv|i|ii|iii|iv)[^-\d\w]*')

# filters out all of the above, aside from TV shows
notMovies = re.compile('^.*\(.*\).*(?:\(.*\)|\{.*\})$')

# filters out TV shows, video games, adult film, etc...
#notMoviesA = re.compile('^(?:\".*|.*\(.*\).*(?:\(.*\)|\{.*\}))$')
notMoviesA = re.compile('^(?:\".*|.*\(.*\).*(?:\{.*\}))$')

def batchOpen(files, encoding=None):
  if encoding == None:
    files = [open(f, 'r') for f in files]
  else:
    files = [codecs.open(f, 'r', encoding) for f in files]
  return itertools.chain.from_iterable(files)

def lineCount(files):
  call = ['wc']
  call.extend(files)
  call.append('-l')
  res = subprocess.check_output(call).decode('utf-8')
  match = fileCountTotal.match(' ' + res)

  if match == None:
    return 0
  else:
    return int(match.group(1))

def scrub(inputStr):
  def removeAccents(inputStr):
    return unicode(''.join([c for c in ud.normalize('NFKD', inputStr) if not ud.combining(c)]))
  def substituteCharacters(inputStr):
    return unicodeSub.sub('-', inputStr)
  def removeCharacters(inputStr):
    return unicodeDel.sub('', inputStr)
  def replaceAnd(inputStr):
    return andSub.sub('and', inputStr)
  def removeEndingTag(inputStr):
    a = inputStr.split('-')
    gen = (x[0] for x in enumerate(reversed(a)) if x[1].isdigit())
    try:
      idx = next(gen)
    except:
      return inputStr
    a = a[0:-1 * idx]
    a[-1] = a[-1][0:-1] + '0'
    return '-'.join(a)
  #  return endingDel.sub('', inputStr)

  text = inputStr.lower()
  text = removeAccents(text)
  text = substituteCharacters(text)
  text = removeCharacters(text)
  text = replaceAnd(text)
  text = removeEndingTag(text)
  text = text.strip('-')

  return text

def isMovie(title):
  match = notMoviesA.match(title)
  return match == None

def prettyPrint(obj, filename):
  f = open(filename, 'w')
  f.write(json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

def reIndex(lst, indexMapping):
  for idx, elem in enumerate(lst):
    indexMapping[elem['id']] = idx
    elem['id'] = idx
