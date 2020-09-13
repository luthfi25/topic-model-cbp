import os
import argparse

######MAIN FUNCTION

# Retrieve Input
parser = argparse.ArgumentParser(description="Augment dataset by the combination of deletion, insertion, synonym, hypernym, and hyponym. will generate AUG-[number of augmentation]-[file name].txt")
parser.add_argument("-dataset", required=True, type=str, help="Dataset file name located in preprocess folder. Don't include 'dataset' and file extension in the file path! [default:]")
parser.add_argument("-aug", type=int, default=1, help="Number of desired augmentation [default:1]")
args = parser.parse_args()

os.system("mkdir ../dataset/{}".format(args.dataset))
os.system("cp ../preprocess/{}.txt ../dataset/{}/{}.txt".format(args.dataset, args.dataset, args.dataset))
print("adding label...")
os.system("python add_label.py ../dataset/{}/{}.txt".format(args.dataset, args.dataset))

print("do normal augmentation with EDA...")
if args.aug < 3:
    # if < 3 directly eda_nlp dataset with aug
    os.system("python eda_nlp/code/augment.py --input=labeled_{}.txt --mode=normal --num_aug={}".format(args.dataset, args.aug))
    os.system("python remove_label.py eda_labeled_{}.txt".format(args.dataset))
    os.system("mv eda_labeled_{}.txt ../dataset/{}/{}aug_{}.txt".format(args.dataset, args.dataset, args.aug, args.dataset))

else:
    # if >= 3 eda_nlp dataset with aug - 2  
    os.system("python eda_nlp/code/augment.py --input=labeled_{}.txt --mode=normal --num_aug={}".format(args.dataset, args.aug - 2))
    os.system("python remove_label.py eda_labeled_{}.txt".format(args.dataset))
    os.system("mv eda_labeled_{}.txt ../dataset/{}/{}aug_{}.txt".format(args.dataset, args.dataset, args.aug - 2, args.dataset))

    print("do hypernym augmentation...")
    # exec hypernym
    os.system("python aug_hypernym.py ../dataset/{}/{}.txt 0.1 normal".format(args.dataset, args.dataset))
    os.system("mv hyp_{}.txt ../dataset/{}/hyp_{}.txt".format(args.dataset, args.dataset, args.dataset))

    print("do hyponym augmentation...")
    # exec hyponym
    os.system("python aug_hyponym.py ../dataset/{}/hyp_{}.txt 0.1 normal".format(args.dataset, args.dataset))
    os.system("mv hypooo_hyp_{}.txt ../dataset/{}/hypooo_hyp_{}.txt".format(args.dataset, args.dataset, args.dataset))

#Removin uneccesary files
os.system("rm -rf labeled_{}.txt".format(args.dataset))
print("all done! please check in 'dataset' folder")