# encoding: utf-8

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

import pandas as pd
import json
import re

import os

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_informal(word):
    try:
        with open("preprocess/informals.json") as informals_json:
            informals_word = json.load(informals_json)
            formal_word = informals_word[word]
            return formal_word
    except KeyError as e:
        formal_input = input("The word \"{}\" is not exist.\nPlease input the correct expansion: ".format(word))
        informals_word[word] = formal_input

        with open("preprocess/informals.json", "w", encoding="utf-8") as informals_json:
            json.dump(informals_word, informals_json, ensure_ascii=False, indent=4)

        return formal_input

def clean_single(sentence):
    #lower case
    sentence = sentence.lower()
    #remove digits
    sentence = re.sub(r'\d', ' ', sentence)
    #remove punctuations
    sentence = re.sub(r'[?!,.();\"\\\/]', ' ', sentence)
    #remove whitespaces
    sentence = re.sub(r'\s\s+', ' ', sentence)

    sentence_split = sentence.split(" ")
    for i in range(len(sentence_split)):
        #convert informal words to formal
        if "'" in sentence_split[i]:
            formal_word = clean_informal(sentence_split[i])
            sentence_split[i] = formal_word
        
        #remove trailing punctuations
        if re.match('^\w*[-:\[\]{}*?!,.();\'\"\\\/]$|^[-:\[\]{}*?!,.();\'\"\\\/]\w*', sentence_split[i]) is not None:
            if(len(sentence_split[i]) > 1):
                new_word = sentence_split[i]
                new_word = new_word[0:len(new_word)-1]
                sentence_split[i] = new_word
            else:
                sentence_split[i] = ""

    #tokenize and lemmatize each words
    word_token = word_tokenize(" ".join(sentence_split))
    filtered = [lemmatizer.lemmatize(w) for w in word_token if (not w in stop_words) and (len(w) > 1)]
    sentence = " ".join(filtered)

    return sentence


def clean(input_dataset, mode):
    #Open file
    dataset_df = pd.read_csv(input_dataset)


    print("Start cleaning {}...".format(input_dataset))
    if mode == "dataset":
        sentences = dataset_df["sentence_english"]
        sentences = [s for s in sentences]

        #remove empty sentence "-"
        while "-" in sentences:
            sentences.remove("-")

        clean_sentences = [clean_single(s) for s in sentences]
        print("Done cleaning!")
        
        return clean_sentences

    elif mode == "background":
        sentences = dataset_df["definition"]
        topics = dataset_df["label"]

        clean_sentences = [clean_single(s) for s in sentences]
        clean_topics = ["_".join(t.strip(" ").split(" ")) for t in topics]
        print("Done cleaning!")

        return clean_sentences, clean_topics
    