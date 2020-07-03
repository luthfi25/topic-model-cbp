import sys

file_name = sys.argv[1] if len(sys.argv) > 1 else ""
mode = sys.argv[2] if len(sys.argv) > 2 else "1"
begin_index = int(sys.argv[3]) if len(sys.argv) > 3 else ""
end_index = int(sys.argv[4]) if len(sys.argv) > 4 else ""

data = []
with open(file_name, "r") as f:
    data = f.readlines()

data = [d.rstrip(" \n").split(" ") for d in data]

total_length = 0
count = {}
for d in data:
    for w in d:
        if w not in count.keys():
            count[w] = 0
        count[w] = count[w] + 1

    total_length += len(d)

if mode != "2":
    sorted_count  = {k: v for k, v in sorted(count.items(), key=lambda item: item[1])}
    print(sorted_count)
    print(len(data))
    print(data[0], data[-1])

    print("Total token: " + str(total_length))
    print("Corpus size (unique token): " + str(len(count.keys())))
    print("Average length: " + str(total_length/len(data)))
else:
    sliced_data = data[begin_index-1:end_index]

    new_count = {}
    new_total_length = 0
    for d in sliced_data:
        for w in d:
            if w not in new_count.keys():
                new_count[w] = 0
            new_count[w] = new_count[w] + 1
        new_total_length += len(d)

    sorted_count = {k: v for k, v in sorted(new_count.items(), key=lambda item: item[1])}
    print(sorted_count)
    print(len(sliced_data))
    print(sliced_data[0], sliced_data[-1])

    print("STATS:")
    print("Total token: " + str(new_total_length))
    print("Corpus size (unique token): " + str(len(new_count.keys())))
    print("Average length: " + str(new_total_length/len(sliced_data)))
