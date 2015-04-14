import codecs
import itertools
import re
import subprocess
import unicodedata as ud

fileCountTotal = re.compile('.* (\d+).*', re.M | re.S)
unicodeDel = re.compile('(?:[\.\'\"\?\!]|[^\x00-\x7f])+')
unicodeSub = re.compile('(?:[\s\-\/\\ \:\(\)\[\]\{\}])+')

# filters out all of the above, aside from TV shows
notMovies = re.compile('^.*\(.*\).*(?:\(.*\)|\{.*\})$')

# filters out TV shows, video games, adult film, etc...
notMoviesA = re.compile('^(?:\".*|.*\(.*\).*(?:\(.*\)|\{.*\}))$')

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
    return u''.join([c for c in ud.normalize('NFKD', inputStr) if not ud.combining(c)])
  def substituteCharacters(inputStr):
    return unicodeSub.sub('-', inputStr)
  def removeCharacters(inputStr):
    return unicodeDel.sub('', inputStr)

  text = inputStr.lower() 
  text = removeAccents(text)
  text = substituteCharacters(text)
  text = removeCharacters(text)
  text = text.strip('-')

  return text

def isMovie(title):
  match = notMoviesA.match(title)
  return match == None
