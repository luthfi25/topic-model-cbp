#using Jensen Shannon Divergence

import sys, math
from scipy.spatial import distance
import ast

file1 = sys.argv[1] if len(sys.argv) > 1 else ""
file2 = sys.argv[2] if len(sys.argv) > 2 else ""

# prob1 = ast.literal_eval(prob1Str)
# prob2 = ast.literal_eval(prob2Str)

probs1 = []
with open(file1, 'r') as f:
    probs1 = f.readlines()
    probs1 = [ast.literal_eval(i) for i in probs1]

probs2 = []
with open(file2, 'r') as f:
    probs2 = f.readlines()
    probs2 = [ast.literal_eval(i) for i in probs2]\

for i in range(0,len(probs1)):
    for j in range(0, len(probs2)):
        print("SIMILARITY "+ str(i) +" and " + str(j) + ": ", str(1 - distance.jensenshannon(probs1[i],probs2[j])))