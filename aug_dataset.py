import os, sys

dataset_arg = sys.argv[1] if len(sys.argv) > 1 else ""

os.system("mkdir {}".format(dataset_arg))
os.system("cp {}.txt {}/{}.txt".format(dataset_arg, dataset_arg, dataset_arg))
os.system("python augmentation/add_label.py {}/{}.txt".format(dataset_arg, dataset_arg))

#STANDARD AUG
os.system("python augmentation/eda_nlp/code/augment.py --input=labeled_{}.txt".format(dataset_arg))
os.system("python augmentation/remove_label.py eda_labeled_{}.txt".format(dataset_arg))
os.system("mv eda_labeled_{}.txt {}/9aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

os.system("python augmentation/eda_nlp/code/augment.py --input=labeled_{}.txt --num_aug=1 ".format(dataset_arg))
os.system("python augmentation/remove_label.py eda_labeled_{}.txt".format(dataset_arg))
os.system("mv eda_labeled_{}.txt {}/1aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

os.system("python augmentation/eda_nlp/code/augment.py --input=labeled_{}.txt --num_aug=12".format(dataset_arg))
os.system("python augmentation/remove_label.py eda_labeled_{}.txt".format(dataset_arg))
os.system("mv eda_labeled_{}.txt {}/12aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

#STANDARD HYPERNYM
os.system("python augmentation/aug_hypernym.py {}/{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hyp_{}.txt {}/hyp_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

os.system("python augmentation/aug_hypernym.py {}/1aug_{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hyp_1aug_{}.txt {}/hyp_1aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

os.system("python augmentation/aug_hypernym.py {}/9aug_{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hyp_9aug_{}.txt {}/hyp_9aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

os.system("python augmentation/aug_hypernym.py {}/12aug_{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hyp_12aug_{}.txt {}/hyp_12aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

#STANDARD HYPONYM
os.system("python augmentation/aug_hyponym.py {}/{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hypooo_{}.txt {}/hypooo_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

os.system("python augmentation/aug_hyponym.py {}/1aug_{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hypooo_1aug_{}.txt {}/hypooo_1aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

os.system("python augmentation/aug_hyponym.py {}/9aug_{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hypooo_9aug_{}.txt {}/hypooo_9aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

os.system("python augmentation/aug_hyponym.py {}/12aug_{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hypooo_12aug_{}.txt {}/hypooo_12aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

#HYPONYM + HYPERNYM
os.system("python augmentation/aug_hyponym.py {}/hyp_{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hypooo_hyp_{}.txt {}/hypooo_hyp_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

os.system("python augmentation/aug_hyponym.py {}/hyp_1aug_{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hypooo_hyp_1aug_{}.txt {}/hypooo_hyp_1aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

os.system("python augmentation/aug_hyponym.py {}/hyp_9aug_{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hypooo_hyp_9aug_{}.txt {}/hypooo_hyp_9aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

os.system("python augmentation/aug_hyponym.py {}/hyp_12aug_{}.txt 0.1".format(dataset_arg, dataset_arg))
os.system("mv hypooo_hyp_12aug_{}.txt {}/hypooo_hyp_12aug_{}.txt".format(dataset_arg, dataset_arg, dataset_arg))

