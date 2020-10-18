import argparse

# Retrieve Input
parser = argparse.ArgumentParser(description="Data statistics extractor. This will generate important stats from your sentence dataset such as top 10 words, number of sentence, average length, and corpus size.")
parser.add_argument("-dataset", required=True, type=str, help="Dataset file name (ONLY txt file) [default:]")
parser.add_argument("-start", default=-1, type=int, help="If you want to limit the source data e.g. generate statistics for 1 company only. Please insert the start index.")
parser.add_argument("-end", default=-1, type=int, help="If you want to limit the source data e.g. generate statistics for 1 company only. Please insert the end index.")
args = parser.parse_args()

data = []
with open(args.dataset, "r") as f:
    data = f.readlines()
    data = [d.rstrip(" \n").split(" ") for d in data]

if args.start != -1 and args.end != -1:
    data = data[args.start-1:args.end]
    print("Showing statistics from index {} to index {}".format(args.start, args.end))

total_length = 0
count = {}
for d in data:
    for w in d:
        if w not in count.keys():
            count[w] = 0
        count[w] = count[w] + 1
    total_length += len(d)

sorted_count ={k:v for k,v in sorted(count.items(), key=lambda item: item[1])}
print("Top 10 words: ", list(reversed(list(sorted_count.keys())[-10:])))
print("Number of sentences: ", str(len(data)))
print("Corpus size: ", str(len(count)))
print("Average word/sentence: ", str(total_length/len(data)))