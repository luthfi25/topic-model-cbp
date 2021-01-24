#using Jensen Shannon Divergence

import sys, math
from scipy.spatial import distance
import ast
import numpy as np

def bhattacharyya(h1, h2):
  '''Calculates the Byattacharyya distance of two histograms.'''

  def normalize(h):
    return h / np.sum(h)

  return 1 - np.sum(np.sqrt(np.multiply(normalize(h1), normalize(h2))))

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

#JS
for i in range(0,len(probs2)):
    for j in range(0, len(probs1)):
        print("JS_SIMILARITY "+ str(i) +" and " + str(j) + ": ", str(1 - distance.jensenshannon(probs2[i],probs1[j])))
    
#Bhattacharyya
for i in range(0,len(probs2)):
    for j in range(0, len(probs1)):
        print("BHATTACHARYYA_SIMILARITY "+ str(i) +" and " + str(j) + ": ", str(1 - bhattacharyya(probs2[i],probs1[j])))
   
#Cosine
for i in range(0,len(probs2)):
    for j in range(0, len(probs1)):
        print("COSINE_SIMILARITY "+ str(i) +" and " + str(j) + ": ", str(1 - distance.cosine(probs2[i],probs1[j])))