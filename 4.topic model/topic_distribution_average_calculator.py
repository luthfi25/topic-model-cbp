import sys
import pandas as pd

theta_file = sys.argv[1] if len(sys.argv) > 1 else ""
dataset_file = sys.argv[2] if len(sys.argv) > 2 else ""
index_file = sys.argv[3] if len(sys.argv) > 3 else ""

theta = []
with open(theta_file, 'r') as f:
    theta = f.readlines()
    theta = [i.rstrip(' \n').split(' ') for i in theta]

dataset = []
with open(dataset_file, 'r') as f:
    dataset = f.readlines()
    dataset = [i.rstrip(' \n').split(' ') for i in dataset]

len_words = [len(i) for i in dataset]
df = pd.read_csv(index_file)

dataset_stats = {}
COMPANY_COUNT = 30
for i in range(0,COMPANY_COUNT+1):
    company_index = df.index[df['company_id'] == i].tolist()
    dataset_stats[i] = {}
    dataset_stats[i]['index'] = company_index
    
    for j in company_index:
        if 'total_words' in dataset_stats[i]:
            dataset_stats[i]['total_words'] += len_words[j]
        else:
            dataset_stats[i]['total_words'] = len_words[j]

average_result = []
TOPIC_COUNT = 26
for i in range(0,COMPANY_COUNT+1):
    company = dataset_stats[i]

    company_result = {
        'company_id': i,
        'average_topic': {}
    }

    for j in range(0, TOPIC_COUNT):
        average_single_topic = 0

        for k in company['index']:
            average_single_topic += (float(theta[k][j]) * len_words[k] / company['total_words'])
        
        average_single_topic = average_single_topic / len(company['index'])
        company_result['average_topic'][j] = average_single_topic
    
    average_result.append(company_result)

for i in average_result:
    for j in range(0, TOPIC_COUNT):
        print(str(i['average_topic'][j]), end=" ")
    print('\n', end= "")