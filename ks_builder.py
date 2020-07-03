import sys
import pandas as pd
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 

import operator
import collections

filename = sys.argv[1] if len(sys.argv) > 1 else ""

dataset = []
with open(filename, 'r') as f:
    dataset = f.readlines()
    dataset = [d.split(" ") for d in dataset]

input_ks = []
for i in range(len(dataset)):
    v = dataset[i][1:]
    topic = dataset[i][0]
    word_occurence = {}

    for word in v:
        word_occurence[word] = v.count(word)
    
    sorted_word_occurence = sorted(word_occurence.items(), key=operator.itemgetter(1), reverse=True)
    sorted_word_occurence = collections.OrderedDict(sorted_word_occurence)
    input_ks.append(topic + ' ' + ' '.join(['%s %s' % (key, value) for (key, value) in sorted_word_occurence.items()]))

with open(filename+"-KS.dat", 'w') as f:
    f.write("\n".join(input_ks))