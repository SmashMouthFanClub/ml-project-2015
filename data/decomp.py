from parse.IMDBAltTitles import parseIMDBAltTitles
from parse.IMDBGenres import parseIMDBGenres
from parse.IMDBKeywords import parseIMDBKeywords
from parse.MovieLensTitles import parseMovieLensTitles
from operator import itemgetter
from util import *

movieFiles = [
  'raw/movies.list.0',
  'raw/movies.list.1',
  'raw/movies.list.2'
]

tagFiles = [
  'raw/keywords.list.0',
  'raw/keywords.list.1',
  'raw/keywords.list.2',
  'raw/keywords.list.3',
  'raw/keywords.list.4'
]

genreFiles = [
  'raw/genres.list.0',
  'raw/genres.list.1'
]

altFiles = [
  'raw/aka-titles.list.0'
]

lensFiles = [
  'raw/movies.dat.0'
]

ratingFiles = [
  'raw/ratings.dat.0',
  'raw/ratings.dat.1',
  'raw/ratings.dat.2',
  'raw/ratings.dat.3',
  'raw/ratings.dat.4',
  'raw/ratings.dat.5'
]

'''
line4Regex = re.compile('^(4)\:')
line5Regex = re.compile('^(5)\:')
movieTitleRegex = re.compile('^((?:\".*?\")|(?:.*?)) \(.*$')
tagCountRegex = re.compile('(.+) \((\d+)')
movieTagRegex = re.compile('^((?:\".*?\")|(?:.*?)) \(.*\t+(.*)$')
genreCountRegex = re.compile('^(.+?)[\t ]+(\d+)$')
lensRegex = re.compile('^(\d+)::(.*?) \(.*?::.*$')
lensArticleRegex = re.compile('^(.*?), ?(The|A|An|Los|Les|La|Le|El|L\')$')
'''

def processMovieLensRatings():
  1

movieID = {}
movieTitle = []
movieTags = []

tagID = {}
tagCount = []

lensID = []

if __name__ == '__main__':

  stats = parseIMDBKeywords(movieID, movieTitle, movieTags, tagID, tagCount, tagFiles)
  print(stats)

  #stats = parseIMDBGenres(movieID, movieTitle, movieTags, tagID, tagCount, genreFiles)
  #print(stats)

  #tagCount[:] = reversed(sorted(tagCount, key = itemgetter(1)))
  #for idx, tag in enumerate(tagCount):
  #  tagID[tag[0]] = idx

  stats = parseIMDBAltTitles(movieID, altFiles)
  print(stats)

  stats = parseMovieLensTitles(movieID, lensID, lensFiles)
  print(stats)

  prettyPrint(movieID, 'movieID.json')
  prettyPrint(lensID, 'mismatch.json')
