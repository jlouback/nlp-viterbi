__author__="Juliana Louback <jl4354@.columbia.edu>"

import sys
from collections import Counter
import fileinput
import logging

"""
python lable_rare.py [input_file]
Read through the input_file, calculate word frequency,
replace words that appear less than 5 times as _RARE_
It modifies the input file directly
"""

#count word frequency, keep hashmap of word(key) and count(value)
data_file = file(sys.argv[1], 'r')
rare_words = Counter(data_file.read().split())
for k in list(rare_words):
	#keep only rare words, count < 5
	if rare_words[k] > 4:
		del rare_words[k]


data_file.close()

#go through the data file
for line in fileinput.input(sys.argv[1], inplace=1):
	parts = line.strip().split(" ")
	word = parts[0]
	#if word is in rare_words list, retag as _RARE_
	if word in rare_words and word != '':
		word = word + " "
		line = line.replace(word, "_RARE_ ")
		sys.stdout.write(line)
		if rare_words[word] == 1:
			del rare_words[word]
	#if word is not in rare_words list, keep original tag
	else:
		sys.stdout.write(line)

data_file.close()






