__author__="Juliana Louback <jl4354@.columbia.edu>"

import sys
from collections import defaultdict
import math
import logging

"""
Used in viterbi.py script
"""

# Return 2 dictionaries containing
# Count(y)
# Count(x~>y)
def count(filename):
	train_counts = file(filename,'r')
	count_y = dict([('O', 0), ('I-MISC', 0), ('I-PER', 0), ('I-ORG', 0), ('I-LOC', 0), ('B-MISC', 0), ('B-PER', 0), ('B-ORG', 0), ('B-LOC', 0)])
	count_xy = dict()

	line = train_counts.readline()
	while line:
		parts = line.strip().split(' ')
		line_type = parts[1]
		# Get Count(y) and Count(x~>y)
		if "WORDTAG" in line_type:
			count = parts[0]
			label = parts[2]
			word = parts[3]
			count_y[label] = count_y[label] + int(float(count))
			if word in count_xy:
				count_xy[word].update({label : count})
			else:
				count_xy[word] = {label : count}
		# Get trigram and bigram counts
		else:
			break

		line = train_counts.readline()

	train_counts.close()
	return count_xy, count_y
