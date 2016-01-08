__author__="Juliana Louback <jl4354@.columbia.edu>"

import sys
from collections import defaultdict
import math
import logging

"""
Usage:
python question5_a.py n-gram_counts [input_file] > [output_file]

Question 5.a: Calculate q(x_i-2, x_i-1, x_i) based on trigram and 
bigram counts produced by count_freqs.py 
(I have selected the n-gram counts from ner_counts)
[input_file] should have three tags per line, separated by a space.

Outputs trigram and it's respective log probability to [output_file]
"""

#map trigram counts from n-gram_counts file 
ngram_counts = file(sys.argv[1], 'r')

trigram_counts = dict()
bigram_counts = dict()

line = ngram_counts.readline()
while line:
	parts = line.strip().split(" ")
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
	line = ngram_counts.readline()

# read input_file, output trigram log probabilities
input_file = file(sys.argv[2], 'r')
line = input_file.readline()
while line:
	parts = line.strip().split(" ")
	y1 = parts[0]
	y2 = parts[1]
	y3 = parts[2]
	bigram = y1 + " " + y2
	trigram = y1 + " " + y2 + " " + y3
	if bigram in bigram_counts and trigram in trigram_counts:
		probability = float(trigram_counts[trigram])/float(bigram_counts[bigram])
		log_probability = math.log(probability)
	else:
		log_probability = 0
	sys.stdout.write("{} {}\n".format(trigram, log_probability))
	line = input_file.readline()

ngram_counts.close()



