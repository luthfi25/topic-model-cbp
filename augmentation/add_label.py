import sys

file_name = sys.argv[1] if len(sys.argv) > 1 else ""
original_file_name = file_name.split("/")[-1]
data = []

with open(file_name, "r") as f:
    data = f.readlines()
    data = [d.rstrip(" \n") for d in data]

new_data = []
for d in data:
    new_d = "1\t" + d
    new_data.append(new_d)

with open("labeled_" + original_file_name, "w") as f:
    f.write("\n".join(new_data))