import os
from preprocess.data_cleaner import run_cleaner
# from augmentation.data_augmenter import run_data_augmenter

#python data_cleaner.py -mode dialog -dataset ../dataset/8.2\ -\ dialog.csv -column sentence_english
dataset_file_path = input("Please input dataset file path: ")
column = input("Column name that holds sentences data: ")
mode = input("Is this a 'dialog' data or a 'background knowledge' data? (choose one) ")
num_aug = input("How many augmentation do you want? (integer) ")
topic_column = "topic_column"

if mode == 'background knowledge':
    mode = 'bk'
    topic_column = input("Column name that holds topic name: ")
elif mode != 'dialog':
    print("Unknown mode!")
    exit()

print("Preprocessing dataset...")

#Create dataset folder
dialog_file_name = dataset_file_path.split("/")[-1].split(".")[0]
os.system("mkdir dataset/{}".format(dialog_file_name))

#Do preprocessing
run_cleaner(mode, dataset_file_path, column, topic_column)

if mode == 'dialog':
    os.system("mv CLEANED-{}.txt dataset/{}/{}.txt".format(dialog_file_name, dialog_file_name, dialog_file_name))
else:
    os.system("mv DESC-{}.txt dataset/{}/DESC-{}.txt".format(dialog_file_name, dialog_file_name, dialog_file_name))
    os.system("mv TOPIC-{}.txt dataset/{}/TOPIC-{}.txt".format(dialog_file_name, dialog_file_name, dialog_file_name))

print("Done preprocessing!")

#Do Augmentation
# run_data_augmenter(dialog_file_name, num_aug, "normal")
# if mode == 'dialog':
#     os.system("python3.7 2.augmentation/data_augmenter.py -mode {} -dataset {} -aug {}".format("normal", dialog_file_name, num_aug))
# else:
#     os.system("python3.7 2.augmentation/data_augmenter.py -mode {} -dataset {} -aug {}".format("bk", dialog_file_name, num_aug))

