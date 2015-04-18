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

def outputUsers(out):
  f = open(out, 'w')
