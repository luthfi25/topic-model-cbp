import sys

file_name = sys.argv[1] if len(sys.argv) > 1 else ""
data = []

with open(file_name, "r") as f:
    data = f.readlines()
    data = [d.rstrip(" \n") for d in data]

old_data = []
for d in data:
    old_d = d.split("1\t")[-1]
    old_data.append(old_d)

with open(file_name, "w") as f:
    f.write("\n".join(old_data))