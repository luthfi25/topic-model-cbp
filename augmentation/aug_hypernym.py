# encoding: utf-8
from nltk.corpus import wordnet
import sys
import random
import math

def compare_word(word1, word2):
    word1_synset = wordnet.synsets(word1)
    word2_synset = wordnet.synsets(word2)

    if len(word1_synset) == 0 or len(word2_synset) == 0:
        return 0
    
    return word1_synset[0].wup_similarity(word2_synset[0])

def get_hypernyms(word):
    hypernyms = set()
    word_wn = wordnet.synsets(word)
    if len(word_wn) == 0:
        return []

    for hyp in word_wn[0].hypernyms():
        for l in hyp.lemmas():
            hypernym = l.name().replace("_", " ").replace("-", " ").lower()
            hypernym = "".join([char for char in hypernym if char in ' qwertyuiopasdfghjklzxcvbnm'])
            hypernyms.add(hypernym) 
    if word in hypernyms:
        hypernyms.remove(word)
    return list(hypernyms)

file_name = sys.argv[1] if len(sys.argv) > 1 else ""
sentences = []
with open(file_name, "r") as f:
    sentences = f.readlines()
    sentences = [s.rstrip(" \n").split(" ") for s in sentences]

degree = sys.argv[2] if len(sys.argv) > 2 else ""
degree = float(degree)

new_sentences = []
for s in sentences:
    # new_s = s.copy()
    new_s = s[:]
    num_replace = math.ceil(degree * len(new_s))
    done_replace = 0

    while done_replace < num_replace:
        word_candidate = random.choice(new_s)
        word_index = new_s.index(word_candidate)
        word_hypernyms = get_hypernyms(word_candidate)
        
        if len(word_hypernyms) > 0:
            hyp_candidate = random.choice(word_hypernyms)
            sim_score = compare_word(word_candidate, hyp_candidate)
            if sim_score > 0.75:    
                print(sim_score, word_candidate, hyp_candidate)
                new_s[word_index] = hyp_candidate
        
        done_replace += 1
    
    new_sentences.append(new_s)

with open('hyp_' + file_name.split("/")[-1], 'w') as f:
    for i in range(len(sentences)):
        old_s = sentences[i]

        f.write(" ".join(old_s) + "\n")

    for i in range(len(new_sentences)):
        old_s = sentences[i]
        new_s = new_sentences[i]

        if old_s != new_s:
            f.write(" ".join(new_s) + "\n")