# encoding: utf-8
# Topic Model for Consensus Building Process
# Muhammad Luthfi

#TODO
#1. Documentation specifying desired input format
#2. Instruction to install java, python3, nltk, pandas, scipy in advance
#3. Fix random seed

#arguments to be parsed from command line
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--input_dataset", required=True, type=str, help="input file of Consensus Building Process dataset in .csv (collection of sentences)")
ap.add_argument("--input_background", required=True, type=str, help="input file of Background Knowledge in .csv (collection of topic-definition pairs)")
args = ap.parse_args()

from pathlib import Path
from preprocess.clean import *
from augmentation.augment import *
from preparation.background_preparation import *
from topic_model.topic_model_executor import *
from finalize.finalize import *

#main function
if __name__ == "__main__":
    #step 1: preprocess
    clean_dataset, companyIDs = clean(args.input_dataset, "dataset")
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

    #step 3: background knowledge preparation
    prepared_background = prepare_background(clean_topic, aug_background, args.input_background)

    #step 3.1: print prepared background knowledge
    with open("dataset/{}/prepared_background.dat".format(background_folder), 'w') as f:
        f.write("\n".join(prepared_background))
    
    #step 4: topic model execution
    results_folder = execute("dataset/{}/hyponym+hypernym+aug_1".format(dataset_folder), dataset_folder, "dataset/{}/prepared_background.dat".format(background_folder), len(prepared_background))

    #step 5: finalization (average topic probability by company & similarity between companies)
    theta = []

    with open(results_folder+dataset_folder+".theta") as f:
        theta = f.readlines()
        theta = [t.split(" ")[:-1] for t in theta]

    topic_probs, similarity_matrix = finalize(theta, companyIDs)

    with open(results_folder+dataset_folder+".average_topic", 'w') as f:
        f.writelines("Company ID\t"+"\t".join(clean_topic)+"\n")
        for c in topic_probs:
            f.writelines(str(c)+"\t"+"\t".join([str(s) for s in topic_probs[c]["topic_probs"]])+"\n")

    with open(results_folder+dataset_folder+".similarity_matrix", "w") as f:
        for c in similarity_matrix:
            f.writelines("Company {}:\t".format(str(c))+"\t".join([str(s) for s in similarity_matrix[c]])+"\n")

    print("All steps finished! Please check dataset folder")