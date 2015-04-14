import math
import os
import shutil
import sys

class ProgressBar:

  startChar = '['
  endChar   = ']'
  emptyChar = '-'
  fullChar  = '='

  def __init__(self, total):
    self.total = total

  def update(self, newPos): 
    (cols, lines) = shutil.get_terminal_size()
    barPos = math.ceil((cols - 2) * newPos / self.total)
    bar = ''.join([ProgressBar.fullChar if x <= barPos else ProgressBar.emptyChar for x in range(1, cols - 1)])
    sys.stdout.write('\r\x1b[K' + ProgressBar.startChar + bar + ProgressBar.endChar)
    sys.stdout.flush()
