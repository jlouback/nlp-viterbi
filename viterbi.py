__author__="Juliana Louback <jl4354@.columbia.edu>"

import sys
from collections import defaultdict
import math
import logging

import emission_counts
import transition_counts

"""
Usage:
python viterbi.py ner.counts ngram.counts ner_dev.dat > [output_file]

Implementation of the Viterbi algorithm

Calculate emission e(x|y) and trigram probability based on data 
in ner_counts,

Read ner_dev.dat, output prediction to [output_file]
"""

# Get Count(y), Count(x~>y), Count(bigram), Count (trigram)
count_xy, count_y = emission_counts.count(sys.argv[1])
bigram_counts, trigram_counts = transition_counts.count(sys.argv[2])

# Go through dev data, predict tag & compute probability based on model above
dev_data = file(sys.argv[3],'r')
log_probability = 0
# First round for q(*, *, y_1)
first_round = True
line = dev_data.readline()
while line:
	word = line.strip()
	# Check for end of sentence
	if word == '':
		sys.stdout.write('\n')
		log_probability = 0
		first_round = True
	else:
		# Check if there is an existing label associated to the word
		if word in count_xy:
			max_probability = 0
			for label in list(count_xy[word]):
				# Calculate e(x|y)
				emission = float(count_xy[word][label]) / float(count_y[label])
				# Calculate q(y| y_i-2, y_i-1)
				# Check for first round
				if first_round:
					y_2 = '*'
					y_1 = '*' 
					first_round = False
				bigram = y_2 + ' ' + y_1
				trigram = y_2 + ' ' + y_1 + ' ' + label
				parameter = 0.0000000001
				if trigram in trigram_counts:
					parameter = float(trigram_counts[trigram])/float(bigram_counts[bigram])
				probability = parameter*emission
				if probability > max_probability:
					max_probability = probability
					arg_max = label	

		# If Count(x~>y) = 0, use _RARE_ 
		else:
			for label in list(count_xy['_RARE_']):
				# Calculate e(_RARE_|y)
				probability = 0
				emission = float(count_xy['_RARE_'][label]) / float(count_y[label])
				# Calculate q(y| y_i-2, y_i-1)
				# Check for first round
				if first_round:
					y_2 = '*'
					y_1 = '*' 
					first_round = False
				bigram = y_2 + ' ' + y_1
				trigram = y_2 + ' ' + y_1 + ' ' + label
				parameter = 0.0000000001
				if trigram in trigram_counts:
					parameter = float(trigram_counts[trigram])/float(bigram_counts[bigram])
				probability = parameter*emission
				if probability > max_probability:
					max_probability = probability
					arg_max = label

		log_probability = log_probability + math.log(max_probability)
		sys.stdout.write("{} {} {}\n".format(word,arg_max,log_probability))
		#Arrange next round of y_i-2, y_i-1
		y_2 = y_1
		y_1 = arg_max
	line = dev_data.readline()

dev_data.close()