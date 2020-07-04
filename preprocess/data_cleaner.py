import argparse
import pandas as pd
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 

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
            new_text = apostrophes[text_split[i]]
            text_split[i] = new_text

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

######MAIN FUNCTION

# Retrieve Input
parser = argparse.ArgumentParser(description="Cleaning dataset, will generated CLEANED-[file_name].txt for dialog dataset, and TOPIC-[file_name].txt and DESC-[file_name].txt for background knowledge dataset.")
parser.add_argument("-mode", required=True, type=str, help="Kind of dataset to be processed (dialog|bk) [default:dialog]")
parser.add_argument("-dataset", required=True, type=str, help="Dataset file name (ONLY csv file) [default:]")
parser.add_argument("-column", required=True, type=str, help="Column name in which sentences exists [default:]")
parser.add_argument("-topic_column", required=False, type=str, help="Column in which topic label exist (only for background knowledge) [default:]")
args = parser.parse_args()

# Sanitize input
file_name = args.dataset
if "/" in file_name:
    file_name = " ".join(args.dataset.split("/")[-1].split(".")[:-1])

if args.mode == "":
    args.mode = "dialog"

# Open file
dataset_df = pd.read_csv(args.dataset)
dataset = dataset_df[args.column]

#Initialize stop wrods and lemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer() 

#list of informal words containing apostrophes
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

print("Begin cleaning....")
if args.mode == "dialog":
    clean_dataset = [clean(d) for d in dataset]

    with open("CLEANED-"+file_name+".txt", 'w') as f:
        f.write("\n".join(clean_dataset))

elif args.mode == "bk":
    if not args.topic_column:
        print("topic_column is empty!")
        exit()
    
    topics = dataset_df[args.topic_column]
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