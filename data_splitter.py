import sys
import pandas as pd
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 

import operator
import collections

apostrophes = dict({
    "don't": "do not",
    "can't": "can not",
    "it's": "it is",
    "i'm": "i am",
    "world's": "world",
    "bird's-eye": "bird eye",
    "president's": "president",
    "there's": "there is",
    "doesn't": "does not",
    "they're": "they are",
    "factory's": "factory",
    "we're": "we are",
    "companies'": "companies",
    "won't": "will not"})

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer() 

def clean(text):

    # #remove stopword
    # word_token = word_tokenize(text)
    # filtered = [lemmatizer.lemmatize(w) for w in word_token if (not w in stop_words) and (len(w) >= 3)]
    # space = " "
    # text = space.join(filtered)
    text = text.lower()
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'[?!,.();\"\\\/]', ' ', text)
    text = re.sub(r'\s\s+', ' ', text)

    text_split = text.split(" ")
    for i in range(len(text_split)):
        if "'" in text_split[i]:
            new_text = apostrophes[text_split[i]]
            text_split[i] = new_text

        if re.match('^\w*[-:\[\]{}*?!,.();\'\"\\\/]$|^[-:\[\]{}*?!,.();\'\"\\\/]\w*', text_split[i]) is not None:
            if(len(text_split[i]) > 1):
                new_text = text_split[i]
                new_text = new_text[0:len(new_text)-1]
                text_split[i] = new_text
            else:
                text_split[i] = ""

    word_token = word_tokenize(" ".join(text_split))
    filtered = [lemmatizer.lemmatize(w) for w in word_token if (not w in stop_words) and (len(w) > 1)]
    text = " ".join(filtered)

    return text

def calculate_stats(dataset):
    total_length = 0
    count = {}
    for d in dataset:
        for w in d.split(" "):
            if w not in count.keys():
                count[w] = 0
            count[w] = count[w] + 1

        total_length += len(d)

    print("Total token: " + str(total_length))
    print("Corpus size (unique token): " + str(len(count.keys())))
    print("Average length: " + str(total_length/len(data)))

def build_ks(topics, dataset):
    input_ks = []
    for i in range(len(dataset)):
        v = clean(dataset[i]).split(" ")
        topic = "_".join(clean(topics[i]).split(" ")) 
        word_occurence = {}

        for word in v:
            word_occurence[word] = v.count(word)
        
        sorted_word_occurence = sorted(word_occurence.items(), key=operator.itemgetter(1), reverse=True)
        sorted_word_occurence = collections.OrderedDict(sorted_word_occurence)
        input_ks.append(topic + ' ' + ' '.join(['%s %s' % (key, value) for (key, value) in sorted_word_occurence.items()]))
    
    return input_ks


filename = sys.argv[1] if len(sys.argv) > 1 else ""
company_val = sys.argv[2] if len(sys.argv) > 2 else ""
split_by = sys.argv[3] if len(sys.argv) > 3 else ""
split_val = sys.argv[4] if len(sys.argv) > 4 else ""

data = pd.read_csv(filename)
clean_datatext = []

if "BK" in filename:
    topics = data['Topics']
    descriptions = data['Descriptions']
    clean_topics = ["_".join(t.strip(" ").split(" ")) for t in topics]
    clean_descriptions = [clean(d) for d in descriptions]

    with open(filename+"-TOPIC.dat", 'w') as f:
        f.write("\n".join(clean_topics))
    
    with open(filename+"-DESC.dat", 'w') as f:
        f.write("\n".join(clean_descriptions))
    exit()
else:
    for index, row in data.iterrows():
        if row["company"] == int(company_val):
            
            if split_by != "":
                if str(row[split_by]) != split_val:
                    continue

            clean_datatext.append(str(row["no"]))

    # calculate_stats(clean_datatext)

# # print("\n".join([d for d in clean_datatext if any(num in d for num in [':', ';', '-', '[', ']', '{', '}', '*'])]))
# print("\n".join([d for d in clean_datatext if any(w for w in d.split(" ") if len(w) == 2 )])))

with open(filename+"-INDEX-company-"+company_val+"-"+split_by+"-"+split_val+"-READY.txt", 'w') as f:
    f.write(",".join(clean_datatext))