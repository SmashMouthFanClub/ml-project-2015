def outputMovies(movieTitle, movieTags, tagID, out):
  def getTagID(tag):
    if tag in tagID:
      return str(tagID[tag])
    else:
      return None

  f = open(out, 'w')

  for i in range(0, len(movieTitle)):
    tags = list(set([x for x in map(getTagID, movieTags[i]) if x is not None]))
    tags = ','.join(tags)
    line = '{}::{}::{}'.format(i, movieTitle[i], tags)
    print(line, file = f)

def outputTags(tagID, tagCount, out):
  f = open(out, 'w')

  for idx, tag in enumerate(tagCount):
    line = '{}::{}::{}'.format(idx, tag[0], tag[1])
    print(line, file = f)

def outputUsers(userRatings, out):
  f = open(out, 'w')

  for idx, user in enumerate(userRatings):
    a = [list(x) for x in zip(*user)]
    movies = ','.join([str(x) for x in a[0]])
    ratings = ','.join([str(x) for x in a[1]])
    line = '{}::{}::{}'.format(idx, movies, ratings)
    print(line, file = f)
