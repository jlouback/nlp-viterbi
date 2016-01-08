__author__="Juliana Louback <jl4354@.columbia.edu>"

import sys
from collections import defaultdict
import math
import logging

"""
Usage:
python question4.py ner.counts ner_dev.dat > [output_file]

Question 4: Calculate emission e(x|y) based on data in ner.counts; 
create entity tagger that returns  y = arg max e(x|y), including log 
probability of each prediction

Read ner_dev.dat, output prediction to [output_file]; 

Note: first run 
python label_rare.py ner_train.dat
python count_freqs.py ner_train.dat > ner.counts
"""

# Calculate the Count(y) for each type of label, as well as Count(x->y), 
# the count of a label y attributed to a word x
train_counts = file(sys.argv[1],"r")

count_y = dict([('O', 0), ('I-MISC', 0), ('I-PER', 0), ('I-ORG', 0), ('I-LOC', 0), ('B-MISC', 0), ('B-PER', 0), ('B-ORG', 0), ('B-LOC', 0)])
count_xy = dict()

line = train_counts.readline()
while line:
	parts = line.strip().split(" ")
	line_type = parts[1]
	if "-GRAM" in line_type:
		break
	count = parts[0]
	label = parts[2]
	word = parts[3]
	count_y[label] = count_y[label] + int(float(count))
	if word in count_xy:
		count_xy[word].update({label : count})
	else:
		count_xy[word] = {label : count}
	line = train_counts.readline()

#Go through dev data, predict arg max e(x|y) based on model above
dev_data = file(sys.argv[2],"r")
line = dev_data.readline()
while line:
	word = line.strip()
	if word == '':	
		sys.stdout.write("\n")
	else:
		max_probability = 0;
		arg_max = "";
		if word in count_xy:
			for label in list(count_xy[word]):
				emission = float(count_xy[word][label]) / float(count_y[label])
				if emission > max_probability:
					max_probability = emission
					arg_max = label
			log_probability = math.log(max_probability)
			sys.stdout.write("{} {} {}\n".format(word, arg_max, log_probability))
		else:
			for label in list(count_y):
				emission = 0;
				if label in count_xy["_RARE_"]:
					emission = float(count_xy["_RARE_"][label]) / float(count_y[label])
				if emission > max_probability:
					max_probability = emission
					arg_max = label
			log_probability = math.log(max_probability)
			sys.stdout.write("{} {} {}\n".format(word, arg_max, log_probability))
	line = dev_data.readline()

train_counts.close()
dev_data.close()








