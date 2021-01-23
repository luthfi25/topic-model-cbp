# encoding: utf-8
import argparse
import pandas as pd
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 

import importlib
import sys

import helper_word

import os

#Initialize stop wrods and lemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer() 

def check_for_apostrophes(word):
    try:
        apostrophes = helper_word.load_apostrophes()
        new_text = apostrophes[word]
        return new_text
    except KeyError as e:
        expansion = input("The word \"{}\" is not exist.\nPlease input the correct expansion: ".format(word))

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "helper_word.py"
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path, "r") as f:
            helper_file = f.readlines()

        with open(abs_file_path, "w") as f:
            last_line = helper_file[-1]
            last_line = last_line[:-2]+",\n"

            for line in helper_file[:-1]:
                f.write(line)
            f.write(last_line)
            f.write('\t"{}": "{}"}})'.format(word, expansion))
        
        importlib.reload(helper_word)
        new_text = check_for_apostrophes(word)
        return new_text


#clean(text), doing preprocessing for a single sentence
def clean(text):
    #Turn into lowercase
    text = text.lower()

    #Remove digits
    text = re.sub(r'\d', ' ', text)
    
    #Remove punctuations
    text = re.sub(r'[?!,.();\"\\\/]', ' ', text)
    
    #Remove whitespaces
    text = re.sub(r'\s\s+', ' ', text)

    text_split = text.split(" ")
    for i in range(len(text_split)):
        
        #Turn informal words
        if "'" in text_split[i]:
            new_word = check_for_apostrophes(text_split[i])
            text_split[i] = new_word

        #Remove trailing punctuations
        if re.match('^\w*[-:\[\]{}*?!,.();\'\"\\\/]$|^[-:\[\]{}*?!,.();\'\"\\\/]\w*', text_split[i]) is not None:
            if(len(text_split[i]) > 1):
                new_text = text_split[i]
                new_text = new_text[0:len(new_text)-1]
                text_split[i] = new_text
            else:
                text_split[i] = ""

    #Tokenize and lemmatize each words
    word_token = word_tokenize(" ".join(text_split))
    filtered = [lemmatizer.lemmatize(w) for w in word_token if (not w in stop_words) and (len(w) > 1)]
    text = " ".join(filtered)

    return text

def run_cleaner(mode, dataset, column, topic_column):
    # Sanitize input
    file_name = dataset
    if "/" in file_name:
        file_name = " ".join(dataset.split("/")[-1].split(".")[:-1])

    if mode == "":
        mode = "dialog"

    # Open file
    dataset_df = pd.read_csv(dataset)

    if "," in column:
        columns = column.split(",")
        dataset = dataset_df[columns[0]] + dataset_df[columns[1]]
    else:
        dataset = dataset_df[column]

    print("Begin cleaning....")
    if mode == "dialog":
        dataset = [d for d in dataset]
        while "-" in dataset:
            dataset.remove("-")
        
        clean_dataset = [clean(d) for d in dataset]

        with open("CLEANED-"+file_name+".txt", 'w') as f:
            f.write("\n".join(clean_dataset))

    elif mode == "bk":
        if not topic_column:
            print("topic_column is empty!")
            exit()
        
        topics = dataset_df[topic_column]
        clean_dataset = [clean(d) for d in dataset]
        clean_topics = ["_".join(t.strip(" ").split(" ")) for t in topics]

        with open("DESC-"+file_name+".txt", 'w') as f:
            f.write("\n".join(clean_dataset))

        with open("TOPIC-"+file_name+".txt", 'w') as f:
            f.write("\n".join(clean_topics))

    else :
        print("Unknown mode! Possible value: (dialog|bk)")
        exit()

    print("Cleaning success!!")

######MAIN FUNCTION

# Retrieve Input
def main():
    parser = argparse.ArgumentParser(description="Cleaning dataset, will generated CLEANED-[file_name].txt for dialog dataset, and TOPIC-[file_name].txt and DESC-[file_name].txt for background knowledge dataset.")
    parser.add_argument("-mode", required=True, type=str, help="Kind of dataset to be processed (dialog|bk) [default:dialog]")
    parser.add_argument("-dataset", required=True, type=str, help="Dataset file name (ONLY csv file) [default:]")
    parser.add_argument("-column", required=True, type=str, help="Column name in which sentences exists, use ',' if there are multiple columns [default:]")
    parser.add_argument("-topic_column", required=False, type=str, help="Column in which topic label exist (only for background knowledge) [default:]")
    args = parser.parse_args()

    run_cleaner(args.mode, args.dataset, args.column, args.topic_column)

if __name__ == "__main__":
    main()