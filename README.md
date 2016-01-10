# NLP - Named Entity tagger with Viterbi algorithm

Code for assignments from prof. Michael Collin's NLP course, COMSW4705 Spring 2015 at Columbia U.

Summary: The Viterbi algorithm finds the maximum probability path for a series of observations, based on emission and transition probabilities. In a Markov Process, emission is the probability of an output given a state and transition is the probability of transitioning to the state given the previous states. In our case, the emission parameter e(x|y) = the probability of the word being x given you attributed tag y. If your training data had 100 counts of 'person' tags, one of which is the word 'London' (I know a guy who named his kid London), e('London'|'person') = 0.01. Now with 50 counts of 'location' tags, 5 of which are 'London', e('London'|'location') = 0.1 which clearly trumps 0.01. The transition parameter q(y<sub>i</sub> | y<sub>i-1</sub>, y<sub>i-2</sub>) = the probability of putting tag y in position i given it's two previous tags. This is calculated by Count(trigram)/Count(bigram). For each word in the development data, he Viterbi algorithm will associate a score for a word-tag combo based on the emission and transition parameters it obtained from the training data. It does this for every possible tag and sees which is more likely. Clearly this won't be 100% correct as natural language is unpredictable, but you should get pretty high accuracy.

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

* **Step 2.** Get bigram and trigram counts:
Python code: transition_counts.py

Pseudocode:
1. Iterate through each line in the n-gram_counts file
1.1 If the line contains ’2-GRAM’ add an item to the bigram_counts dictionary using the bigram (two space-separated labels following the tag type '2-gram') as key, count as value. This dictionary will contain Count(y<sub>i-2</sub>,y<sub>i-1</sub>).
1.2 If the line contains ’3-GRAM’, add an item to the trigram_counts dictionary using the trigram as key, count as value. This dictionary will contain Count(y<sub>i-2</sub>, y<sub>i-1</sub>, y<sub>i</sub>).
2. Return dictionaries of bigram and trigram counts.

* **Step 3.** Viterbi:
(For each line in the [input_file]):
1. If the word was seen in training data (present in the count_xy dictionary), for each of the possible labels for the word:
1.1 Calculate emission = count_xy[word][label] / float(count_y[label]
1.2 Calculate transition = trigram_counts[trigram])/float(bigram_counts[bigram] Note: y<sub>i-2</sub> = *, y<sub>i-1</sub> = * for the first round
1.3 Set probability = emission x transition
1.4 Update max(probability) and arg max if needed.
2 If the word was not seen in the training data:
2.1 Calculate emission = count xy[_RARE_][label] / float(count y[label].
2.2 Calculate q(y<sub>i</sub>|y<sub>i-1</sub>, y<sub>i-2</sub>) = trigram counts[trigram])/float(bigram counts[bigram]. Note: y<sub>i-2</sub> = ∗, y<sub>i-1</sub> = ∗ for the first round
2.3 Set probability = emission ×q(y<sub>i</sub>|y<sub>i-1</sub>, y<sub>i-2</sub>).
2.4 Update max(probability) if needed, arg max = _RARE_
3. Write arg max and log(max(probability)) to output file.
4. Update y<sub>i-2</sub>, y<sub>i-1</sub>.


## Evaluation
Prof. Michael Collins provided an evaluation script to verify the output of your Viterbi implementation.
Usage: python eval_ne_tagger.py ner_dev.key [output_file]