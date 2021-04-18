# encoding: utf-8
# Topic Model for Consensus Building Process
# Muhammad Luthfi

#TODO
#1. Documentation specifying desired input format
#2. Instruction to install nltk, pandas in advance
#3. Proceed with topic model and finalization

#arguments to be parsed from command line
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--input_dataset", required=True, type=str, help="input file of Consensus Building Process dataset in .csv (collection of sentences)")
ap.add_argument("--input_background", required=True, type=str, help="input file of Background Knowledge in .csv (collection of topic-definition pairs)")
args = ap.parse_args()

from pathlib import Path
from preprocess.clean import *
from augmentation.augment import *

#main function
if __name__ == "__main__":
    #step 1: preprocess
    clean_dataset = clean(args.input_dataset, "dataset")
    clean_background, clean_topic = clean(args.input_background, "background")

    #step 1.1: print cleaned documents
    dataset_folder = args.input_dataset.split("/")[-1].split(".")[0]
    background_folder = args.input_background.split("/")[-1].split(".")[0]

    Path("dataset/{}".format(dataset_folder)).mkdir(parents=True, exist_ok=True)
    Path("dataset/{}".format(background_folder)).mkdir(parents=True, exist_ok=True)

    with open("dataset/{}/cleaned_dataset.txt".format(dataset_folder), 'w') as f:
        f.write("\n".join(clean_dataset))
    
    with open("dataset/{}/cleaned_background.txt".format(background_folder), 'w') as f:
        f.write("\n".join(clean_background))
    
    #step 2: augmentation
    aug_dataset = augment(dataset_folder, clean_dataset, 1, True, args.input_dataset)
    aug_background = augment(background_folder, clean_background, 12, True, args.input_background)