EXTENSION_DEGREE = 0.1

def add_label(input_eda, dataset):
    labeled = ["1\t"+d for d in dataset]

    with open(input_eda, 'w') as f:
        f.write("\n".join(labeled))

def remove_label(output_eda):
    data = []

    with open(output_eda, "r") as f:
        data = f.readlines()
        data = [d.rstrip(" \n") for d in data]
    
    old_data = [d.split("1\t")[-1] for d in data]
    
    with open(output_eda, "w") as f:
        f.write("\n".join(old_data))
    
    return old_data

import math
import random
from nltk.corpus import wordnet

def get_extension(word, mode):
    extension_set = set()
    word_wn = wordnet.synsets(word)
    if len(word_wn) == 0:
        return []
    
    extension_source = word_wn[0].hypernyms() if mode == "hypernym" else word_wn[0].hyponyms()

    for hyp in extension_source:
        for l in hyp.lemmas():
            hyp_word = l.name().replace("_", " ").replace("-", " ").lower()
            hyp_word = "".join([char for char in hyp_word if char in ' qwertyuiopasdfghjklzxcvbnm'])
            extension_set.add(hyp_word)

    if word in extension_set:
        extension_set.remove(word)
    
    return list(extension_set)

def compare_word(word1, word2):
    word1_synset = wordnet.synsets(word1)
    word2_synset = wordnet.synsets(word2)
    
    if len(word1_synset) == 0 or len(word2_synset) == 0:
        return 0
    
    return word1_synset[0].wup_similarity(word2_synset[0])


def do_aug_extension(aug_dataset, mode):
    aug_extended_dataset = []
    for d in aug_dataset:
        new_d = d.split(" ")
        num_replace = math.ceil(EXTENSION_DEGREE * len(new_d))
        done_replace = 0

        while done_replace < num_replace:
            word_candidate = random.choice(new_d)
            word_index = new_d.index(word_candidate)
            word_hyp = get_extension(word_candidate, mode)

            if len(word_hyp) > 0:
                hyp_candidate = random.choice(word_hyp)
                sim_score = compare_word(word_candidate, hyp_candidate)
                if sim_score > 0.75:
                    print(sim_score, word_candidate, hyp_candidate)
                    new_d[word_index] = hyp_candidate

            done_replace += 1
        
        aug_extended_dataset.append(" ".join(new_d))
    
    return aug_dataset, aug_extended_dataset


import os

def augment(dataset_folder, dataset, num_aug, doAugExtension, placeHolderText):
    print("augmenting {}...".format(placeHolderText))
    input_eda = "dataset/{}/labeled.txt".format(dataset_folder)

    print("adding label...")
    add_label(input_eda, dataset)

    print("do normal augmentation with EDA...")
    os.system("python augmentation/eda_nlp/code/augment.py --input={} --num_aug={}".format(input_eda, num_aug))

    print("done augmentating, processing output...")
    aug_dataset = remove_label("dataset/{}/eda_labeled.txt".format(dataset_folder))
    os.system("mv dataset/{}/eda_labeled.txt dataset/{}/aug_{}".format(dataset_folder, dataset_folder, num_aug))
    os.system("rm -rf {}".format(input_eda))

    #should we do hypernym and hyponym augmentation?
    if doAugExtension:
        print("do hypernym augmentation...")
        aug_dataset, hypernym_dataset = do_aug_extension(aug_dataset, "hypernym")

        #combine aug_dataset with hypernym_dataset
        for i in range(len(aug_dataset)):
            aug_dataset[i] = aug_dataset[i] + " " + hypernym_dataset[i] if aug_dataset[i] != hypernym_dataset[i] else aug_dataset[i]

        with open("dataset/{}/hypernym+aug_{}".format(dataset_folder, num_aug), 'w') as f:
            f.write("\n".join(aug_dataset))
        
        print("do hyponym augmentation...")
        aug_dataset, hyponym_dataset = do_aug_extension(aug_dataset, "hyponym")

        #combine aug_dataset with hypernym_dataset
        for i in range(len(aug_dataset)):
            aug_dataset[i] = aug_dataset[i] + " " + hyponym_dataset[i] if aug_dataset[i] != hyponym_dataset[i] else aug_dataset[i]

        with open("dataset/{}/hyponym+hypernym+aug_{}".format(dataset_folder, num_aug), 'w') as f:
            f.write("\n".join(aug_dataset))
    
    print("Done augmentation!")
    return aug_dataset

    