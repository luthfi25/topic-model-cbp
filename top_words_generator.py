import sys

phi_filename = sys.argv[1] if len(sys.argv) > 1 else ""
vocab_filename = sys.argv[2] if len(sys.argv) > 2 else ""

phi_str = []
topic_names = []
with open(phi_filename, "r") as f:
    phi_str = f.readlines()
    phi_str = [p.rstrip(" \n").split(" ") for p in phi_str]
    topic_names = [p[0] for p in phi_str]
    phi_str = [p[1:] for p in phi_str]

#turn phi into float
phi = []
for p in phi_str:
    phi.append([float(txt) for txt in p])


vocab = {}
with open(vocab_filename, "r") as f:
    vocab_lst = f.readlines()
    vocab_lst = [v.rstrip(" \n").split(" ") for v in vocab_lst]
    for v in vocab_lst:
        vocab[int(v[1])] = v[0]

print(len(phi))
print(len(phi[0]))
# print(phi[0])

sorted_phi = []
for p in phi:
    sorted_p_index = [i[0] for i in sorted(enumerate(p), key=lambda x:x[1])]
    sorted_p_val = [i[1] for i in sorted(enumerate(p), key=lambda x:x[1])]
    sorted_p_val.reverse()
    sorted_p_index.reverse()
    # print(sorted_p_val[:3])
    sorted_phi.append(sorted_p_index[:10])

print(sorted_phi)

#generate new phi.dat
with open("NEW-phi.dat", "w") as f:
    for i in range(len(sorted_phi)):
        f.write(topic_names[i] + " ")
        for p in sorted_phi[i]:
            f.write(vocab[p] + " ")
        f.write("\n")