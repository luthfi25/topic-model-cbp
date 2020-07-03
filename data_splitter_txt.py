import sys

file_name = sys.argv[1] if len(sys.argv) > 1 else ""
index_file_name = sys.argv[2] if len(sys.argv) > 2 else ""

index = []
with open(index_file_name, 'r') as f:
    index = f.readlines()
    index = index[0].rstrip(" \n").split(",")
    index = [int(i)-1 for i in index]

sentences = []
with open(file_name, 'r') as f:
    sentences = f.readlines()
    sentences = [" ".join(sentences[i].rstrip(" \n").split(" ")[1:]) for i in index]

file_name_clean = file_name.split("/")[-1]
index_file_name_clean = index_file_name.split("/")[-1]

with open("SPLITTEDby-"+index_file_name_clean+"-"+file_name_clean, "w") as f:
    f.write("\n".join(sentences))