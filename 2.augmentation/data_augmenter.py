import os
import argparse

######MAIN FUNCTION
####TODO:
# 1. Handler error in aug_hyponym.py: UnicodeDecodeError: 'ascii' codec can't decode byte 0xe2 in position 0: ordinal not in range(128)
# 2. Validate hypernym and hypnonym, create mapping from original sentence to new sentences
# 3. Clean and tidy working folder, create new working folder
# 4. Remaining steps: Data preparation step (making .dat files for both dialog and bk), Topic model implementation step, Finalisation step (calculating convergence and top words)

# Retrieve Input
parser = argparse.ArgumentParser(description="Augment dataset by the combination of deletion, insertion, synonym, hypernym, and hyponym. will generate AUG-[number of augmentation]-[file name].txt")
parser.add_argument("-dataset", required=True, type=str, help="Dataset file name located in preprocess folder. Don't include 'preprocess' and file extension in the file path! [default:]")
parser.add_argument("-aug", type=int, default=1, help="Number of desired augmentation [default:1]")
parser.add_argument("-mode", default="normal", required=False, type=str, help="Kind of dataset to be processed (normal|bk) [default:normal]")
args = parser.parse_args()

os.system("mkdir ../dataset/{}".format(args.dataset))
os.system("cp ../1.preprocess/{}.txt ../dataset/{}/{}.txt".format(args.dataset, args.dataset, args.dataset))
print("adding label...")
os.system("python add_label.py ../dataset/{}/{}.txt".format(args.dataset, args.dataset))

print("do normal augmentation with EDA...")
if args.aug < 3:
    # if < 3 directly eda_nlp dataset with aug
    os.system("python eda_nlp/code/augment.py --input=labeled_{}.txt --mode={} --num_aug={}".format(args.dataset, args.mode, args.aug))
    os.system("python remove_label.py eda_labeled_{}.txt".format(args.dataset))
    os.system("mv eda_labeled_{}.txt ../dataset/{}/{}aug_{}.txt".format(args.dataset, args.dataset, args.aug, args.dataset))

else:
    # if >= 3 eda_nlp dataset with aug - 2  
    os.system("python eda_nlp/code/augment.py --input=labeled_{}.txt --mode={} --num_aug={}".format(args.dataset, args.mode, args.aug - 2))
    os.system("python remove_label.py eda_labeled_{}.txt".format(args.dataset))
    os.system("mv eda_labeled_{}.txt ../dataset/{}/{}aug_{}.txt".format(args.dataset, args.dataset, args.aug - 2, args.dataset))

    print("do hypernym augmentation...")
    # exec hypernym
    os.system("python aug_hypernym.py ../dataset/{}/{}aug_{}.txt 0.1 {}".format(args.dataset, args.aug - 2, args.dataset, args.mode))
    os.system("mv hyp_{}aug_{}.txt ../dataset/{}/hyp_{}aug_{}.txt".format(args.aug - 2, args.dataset, args.dataset, args.aug - 2, args.dataset))

    print("do hyponym augmentation...")
    # exec hyponym
    os.system("python aug_hyponym.py ../dataset/{}/hyp_{}aug_{}.txt 0.1 {}".format(args.dataset, args.aug - 2, args.dataset, args.mode))
    os.system("mv hypooo_hyp_{}aug_{}.txt ../dataset/{}/hypooo_hyp_{}aug_{}.txt".format(args.aug - 2, args.dataset, args.dataset, args.aug - 2, args.dataset))

#Removin uneccesary files
os.system("rm -rf labeled_{}.txt".format(args.dataset))
print("all done! please check in 'dataset' folder")