__author__="Juliana Louback <jl4354@.columbia.edu>"

import sys
from collections import defaultdict
import math
import logging

"""
Used in viterbi.py script
"""

# Return 2 dictionaries containing:
# Count(bigram)
# Count (trigram)
def count(filename):
	ngram_counts = file(filename, 'r')

	trigram_counts = dict()
	bigram_counts = dict()

	line = ngram_counts.readline()
	while line:
		parts = line.strip().split(' ')
		count = parts[0]
		gram_type = parts[1]
		if "2-" in gram_type:
			y1 = parts[2]
			y2 = parts[3]
			bigram = y1 + ' ' + y2
			bigram_counts[bigram] = count
		elif "3-" in gram_type:
			y1 = parts[2]
			y2 = parts[3]
			y3 = parts[4]
			trigram = y1 + ' ' + y2 + ' ' + y3
			trigram_counts[trigram] = count
		line = ngram_counts.readline()

	ngram_counts.close()
	return bigram_counts, trigram_counts



