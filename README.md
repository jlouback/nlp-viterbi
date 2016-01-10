# NLP - Named Entity tagger with Viterbi algorithm

Code for assignments from prof. Michael Collin's NLP course, COMSW4705 Spring 2015 at Columbia U.

* **Optional Preprocessing.**
Re-label words in training data with frequency < 5 as '_RARE_' - This isn't required, but useful. Re-run count_freqs.py if used.
Python code: label rare.py
Usage: python label_rare.py [input_file]
Pseudocode:
1. Uses Python Counter to obtain word counts in [input_file]; removes all word-count pairs with count < 5, store remaining pairs in a dictionary named rare_words.
2. Iterates through each line in [input file], checks if word is in rare words dictionary, if so, replaces word with _RARE_.


* **Step 1.** Get Count(y) and Count(x~y):
Python code: emission_counts.py
Pseudocode:
1. Iterate through each line in ner.counts file:
1.1 Store each word-label-count combo in a dictionary count xy containing a dictionary for each word encountered. Each word dictionary contains key-value pairs of the label given to the word and its respective counter. i.e. count xy[Peter][I-PER] returns the number of times the word ‘Peter’ was labeled ‘I-PER’ in the training data.
1.2 The dictionary count y contains 8 items, one for each label ( RARE , O, I-MISC, I-PER, I-ORG, I-LOC, B-MISC, B-PER, B-ORG, B-LOC); at each line, add the count to its respective label in count y to obtain the absolute tag frequency, Count(y).

* **Step 2.** Get bigram and trigram counts.
Python code: transition_counts.py
Pseudocode:
1. Iterate through each line in the n-gram_counts file
1.1 If the line contains ’2-GRAM’ add an item to the bigram_counts dictionary using the bigram (two space-separated labels following the tag type '2-gram') as key, count as value. This dictionary will contain Count(yi−2,yi−1).
1.2 If the line contains ’3-GRAM’, add an item to the trigram_counts dictionary using the trigram as key, count as value. This dictionary will contain Count(yi−2, yi−1, yi).
2. Return dictionaries of bigram and trigram counts.

* **Step 3.** Viterbi:
(For each line in the [input_file]):
1. If the word was seen in training data (present in the count_xy dictionary), for each of the possible labels for the word:
1.1 Calculate emission = count_xy[word][label] / float(count_y[label]
1.2 Calculate transition = trigram_counts[trigram])/float(bigram_counts[bigram] Note: yi−2 = *, yi−1 = * for the first round
1.3 Set probability = emission x transition
1.4 Update max(probability) and arg max if needed.
2 If the word was not seen in the training data:
2.1 Calculate emission = count xy[_RARE_][label] / float(count y[label].
2.2 Calculate q(yi|yi−1, yi−2) = trigram counts[trigram])/float(bigram counts[bigram]. Note: yi−2 = ∗, yi−1 = ∗ for the first round
2.3 Set probability = emission ×q(yi|yi−1, yi−2).
2.4 Update max(probability) if needed, arg max = _RARE_
3. Write arg max and log(max(probability)) to output file.
4. Update yi−2, yi−1.


## Evaluation
Prof. Michael Collins provided an evaluation script to verify the output of your Viterbi implementation.
Usage: python eval_ne_tagger.py ner_dev.key [output_file]