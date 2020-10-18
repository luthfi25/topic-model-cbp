import argparse
import operator
import collections
import os

# Retrieve Input
parser = argparse.ArgumentParser(description="Build background knowledge file in a proper .dat format")
parser.add_argument("-topic", required=True, type=str, help="Topic file location. Please input full path but without extention. [default:]")
parser.add_argument("-desc", required=True, type=str, help="Description file location. Please input the already augmented file. Please input full path but without extention. [default:]")
args = parser.parse_args()

topics = []
descriptions = []
bk_name = args.desc.split("/")[-1].split(".")[0].split("_")[-1]

with open(args.topic, "r") as f:
    topics = f.readlines()

with open(args.desc, "r") as f:
    descriptions = f.readlines()
    descriptions = [s.split(" ") for s in descriptions]

input_ks = []
print("Begin calculating...")
for i in range(len(topics)):
    desc = descriptions[i]
    topic = topics[i]
    word_occurence = {}

    for word in desc:
        word_occurence[word] = desc.count(word)
    
    sorted_word_occurence = sorted(word_occurence.items(), key=operator.itemgetter(1), reverse=True)
    sorted_word_occurence = collections.OrderedDict(sorted_word_occurence)
    input_ks.append(topic + ' ' + ' '.join(['%s %s' % (key, value) for (key, value) in sorted_word_occurence.items()]))

print("Finished calculating! Ready to print...")
dat_file_name = "READY-BK-{}.dat".format(bk_name)
with open(dat_file_name, "w") as f:
    f.write("\n".join(input_ks))

os.system("cp {} ../dataset/{}/{}".format(dat_file_name, bk_name, dat_file_name))
os.system("rm -rf {}".format(dat_file_name))
print("All done!")