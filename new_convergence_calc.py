import sys, math
from scipy.spatial import distance

theta_file_name = sys.argv[1] if len(sys.argv) > 1 else ""
index_file_name = sys.argv[2] if len(sys.argv) > 2 else ""
mode = sys.argv[3] if len(sys.argv) > 3 else ""

def entropy(prob_dist, base=math.e):
    return -sum([float(p) * math.log(float(p),base) for p in prob_dist if p != 0])

def jsd(prob_dists, base=math.e):
    weight = 1/len(prob_dists) #all same weight
    js_left = []
    for i in range(0, len(prob_dists[0])):
        js_left.append(0)

    js_right = 0    
    for pd in prob_dists:
        for i in range(0, len(pd)):
            js_left[i] += float(pd[i])*weight

        js_right += weight*entropy(pd,base)
    return entropy(js_left)-js_right

index = []
with open(index_file_name, 'r') as f:
    index = f.readlines()
    index = index[0].rstrip(" \n").split(",")
    index = [int(i)-1 for i in index]

theta = []
with open(theta_file_name, 'r') as f:
    theta = f.readlines()
    theta = [theta[i].rstrip(" \n").split(" ")[1:] for i in index]

print(theta)

if mode == "TOPIC":
    sum_theta = []
    first_line = True
    for t in theta:
        for i in range(0, len(t)):
            if first_line:
                sum_theta.append(float(t[i]))
            else:
                sum_theta[i] += float(t[i])
        first_line = False
    
    sum_theta = [t/len(index) for t in sum_theta]
    print(sum_theta)
    exit()

print("TEST: ", str(1 - jsd([[0.5, 0.5],[0.1, 0.9]])))
print("TOTAL AVERAGE: " + str(1- jsd(theta)))