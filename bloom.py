#David Lichtenberg
#DMLICHT
#Dlichte5@jhu

#This is a toy implementation of a bloom filter.
#I built it to better understand how they work and to play
#with pytest for the first time.

import zlib
import itertools
import string

class BloomFilter(object):
  """Bloom Filter data structure toy implementation 
  with k=2 hashing function"""

  def __init__(self, size):
    self.size = size
    self.bit_array = [0]*self.size

  def insert(self, element):
    """sets hashed bits to on in array"""
    h1, h2 = self._get_hashed_values(element)
    self.bit_array[h1] = 1
    self.bit_array[h2] = 1

  def query(self, element):
    """checks if element is present in set,
    note this allows for false positive."""
    h1, h2 = self._get_hashed_values(element)
    return self.bit_array[h1] and self.bit_array[h2]

  def _get_hashed_values(self, element):
    h1 = zlib.adler32(element) % self.size
    h2 = zlib.crc32(element) % self.size
    return h1, h2

def test_bloom_correctly_returns_false():
  unadded_string = "I haven't been added"
  bloom = BloomFilter(100)
  assert bloom.query(unadded_string) == False

def test_bloom_correctly_returns_true():
  added_string = "I have been added"
  bloom = BloomFilter(100)
  bloom.insert(added_string)
  assert bloom.query(added_string) == True

def test_three_letter_words():
  words_to_add = ["car", "hat", "map"]
  bloom = BloomFilter(10000000)
  map(bloom.insert, words_to_add)
  num_hits = 0
  for three_letter_list in itertools.permutations(string.lowercase, 3):
    s = ''.join(three_letter_list)
    if bloom.query(s):
      in_word_list = s in words_to_add
      assert in_word_list
      num_hits += 1
  assert num_hits == len(words_to_add)
