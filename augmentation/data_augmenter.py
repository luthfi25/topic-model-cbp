import os
import argparse
import add_label

# Retrieve Input
parser = argparse.ArgumentParser(description="Augment dataset by the combination of deletion, insertion, synonym, hypernym, and hyponym. will generate AUG-[number of augmentation]-[file name].txt")
parser.add_argument("-dataset", required=True, type=str, help="Dataset file name located in preprocess folder. Don't include 'preprocess' and file extension in the file path! [default:]")
parser.add_argument("-aug", type=int, default=1, help="Number of desired augmentation [default:1]")
parser.add_argument("-mode", default="normal", required=False, type=str, help="Kind of dataset to be processed (normal|bk) [default:normal]")
args = parser.parse_args()

def run_data_augmenter(dataset, aug, mode):
    folder_name = "../dataset/{}/".format(dataset)
    file_name = "{}.txt".format(dataset)

    # if mode == "normal":
    #     file_name = "{}.txt".format(dataset)
    # else:
    #     file_name = "{}.txt".format(dataset)

    print("adding label...")
    add_label.run_add_label(folder_name+file_name)

    print("do normal augmentation with EDA...")
    if aug < 3:
        # if < 3 directly eda_nlp dataset with aug
        abs_dir = os.getcwd()

        os.system("python "+abs_dir+"/eda_nlp/code/augment.py --input=labeled_{}.txt --mode={} --num_aug={}".format(dataset, mode, aug))
        os.system("python remove_label.py eda_labeled_{}.txt".format(dataset))
        os.system("mv eda_labeled_{}.txt ../dataset/{}/{}aug_{}.txt".format(dataset, dataset, aug, dataset))

    else:
        # if >= 3 eda_nlp dataset with aug - 2  
        os.system("python eda_nlp/code/augment.py --input=labeled_{}.txt --mode={} --num_aug={}".format(dataset, mode, aug - 2))
        os.system("python remove_label.py eda_labeled_{}.txt".format(dataset))
        os.system("mv eda_labeled_{}.txt ../dataset/{}/{}aug_{}.txt".format(dataset, dataset, aug - 2, dataset))

        print("do hypernym augmentation...")
        # exec hypernym
        os.system("python aug_hypernym.py ../dataset/{}/{}aug_{}.txt 0.1 {}".format(dataset, aug - 2, dataset, mode))
        os.system("mv hyp_{}aug_{}.txt ../dataset/{}/hyp_{}aug_{}.txt".format(aug - 2, dataset, dataset, aug - 2, dataset))

        print("do hyponym augmentation...")
        # exec hyponym
        os.system("python aug_hyponym.py ../dataset/{}/hyp_{}aug_{}.txt 0.1 {}".format(dataset, aug - 2, dataset, mode))
        os.system("mv hypooo_hyp_{}aug_{}.txt ../dataset/{}/hypooo_hyp_{}aug_{}.txt".format(aug - 2, dataset, dataset, aug - 2, dataset))

    #Removin uneccesary files
    os.system("rm -rf labeled_{}.txt".format(dataset))
    print("all done! please check in 'dataset' folder")

if __name__ == "__main__":
    run_data_augmenter(args.dataset, args.aug, args.mode)