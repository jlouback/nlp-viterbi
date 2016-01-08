__author__="Juliana Louback <jl4354@.columbia.edu>"

import sys
from collections import defaultdict
import math
import logging

"""
Usage:
python question5_b.py ner.counts ner_dev.dat > [output_file]

Question 5.a: Implementation of the Viterbi algorithm

Calculate emission e(x|y) and trigram probability based on data 
in ner_counts 

Read ner_dev.dat, output prediction to [output_file];
"""

# Obtain the Count(y) for each type of lable, as well as Count(x~>y), 
# to calculate emission; then trigram and bigram frequencies
train_counts = file(sys.argv[1],"r")
count_y = dict([('O', 0), ('I-MISC', 0), ('I-PER', 0), ('I-ORG', 0), ('I-LOC', 0), ('B-MISC', 0), ('B-PER', 0), ('B-ORG', 0), ('B-LOC', 0)])
count_xy = dict()
trigram_counts = dict()
bigram_counts = dict()

line = train_counts.readline()
while line:
	parts = line.strip().split(" ")
	line_type = parts[1]
	# Get Count(y) and Count(x~>y)
	if "WORDTAG" in line_type:
		count = parts[0]
		lable = parts[2]
		word = parts[3]
		count_y[lable] = count_y[lable] + int(float(count))
		if word in count_xy:
			count_xy[word].update({lable : count})
		else:
			count_xy[word] = {lable : count}
	line = train_counts.readline()

	# Get trigram and bigram counts
	else:
		count = parts[0]
		gram_type = parts[1]
		if "2-" in gram_type:
			y1 = parts[2]
			y2 = parts[3]
			bigram = y1 + " " + y2
			bigram_counts[bigram] = count
		elif "3-" in gram_type:
			y1 = parts[2]
			y2 = parts[3]
			y3 = parts[4]
			trigram = y1 + " " + y2 + " " + y3
			trigram_counts[trigram] = count
	line = train_counts.readline()

logging.warning(count_y)
# Go through dev data, predict tag & compute probability based on model above
dev_data = file(sys.argv[2],"r")
log_probability = 0;
# First round for q(*, *, y_1)
first_round = True
line = dev_data.readline()
while line:
	word = line.strip()
	# Check for end of sentence
	if word == '':
		sys.stdout.write("\n")
		log_probability = 0;
		first_round = True
	else:
		# Check if there is an existing lable associated to the word
		if word in count_xy:
			max_probability = 0;
			arg_max = "";
			for lable in list(count_xy[word]):
				# Calculate e(x|y)
				emission = float(count_xy[word][lable]) / float(count_y[lable])

				# Calculate q(y| y_i-2, y_i-1)
				# Check for first round
				if first_round:
					y_2 = "*"
					y_1 = "*" 
					first_round = False
				bigram = y_2 + " " + y1
				trigram = y_2 + " " + y1 + " " + lable
				# If trigram and bigram do not exist, replace with 1
				if bigram in bigram_counts and trigram in trigram_counts:
					parameter = float(trigram_counts[trigram])/float(bigram_counts[bigram])
				else:
					parameter = 1
				probability = parameter * emission
				if probability > max_probability:
					max_probability = probability
					arg_max = lable
		# If Count(x~>y) = 0, use _RARE_ 
		else:
			# Check for first round
			if first_round:
				y_2 = "*"
				y_1 = "*" 
				first_round = False
			for lable in list(count_y):
				# Calculate e(_RARE_|y)
				if lable in count_xy["_RARE_"]:
					emission = float(count_xy["_RARE_"][lable]) / float(count_y[lable])
				# Calculate q(y| y_i-2, y_i-1)
				bigram = y_2 + " " + y1
				trigram = y_2 + " " + y1 + " " + lable
				# If trigram and bigram do not exist, replace with 1
				if bigram in bigram_counts and trigram in trigram_counts:
					parameter = float(trigram_counts[trigram])/float(bigram_counts[bigram])
				else:
					parameter = 1
				probability = parameter * emission
				if probability > max_probability:
					max_probability = probability
					arg_max = lable
			log_probability = math.log(max_probability)

	# As the log of a product is the sum of the logs:
	log_probability = log_probability + math.log(max_probability)
	sys.stdout.write("{} {} {}\n".format(word, arg_max, log_probability))
	# Arrange next round of y_i-2, y_i-1
	y2 = y1
	y1 = arg_max
	line = dev_data.readline()

train_counts.close()
dev_data.close()