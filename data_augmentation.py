import numpy  as np 
import pandas as pd
from random import randint
from processing import *

fs = 256
interval = 20
k = 10

filenames = ['avatar1', 'avengers1', 'bbc1', 'bear1', 'bighero1', 'creed1', 'edgeoftmr11', 'gunviolence1', 'ironman1', 'joe1', 'lex1', 'vox1']
files = [pd.read_csv(('datasets/{}.csvprocessed.csv').format(name)) for name in filenames]

data_sets = pd.concat(files, ignore_index=True).dropna()
labels = data_sets["Interest"]
    
labels_norm = [1 if x == 4 or x == 5 else 0 for x in labels]

data_sets["Interest"] = labels_norm

interested = np.array(data_sets[data_sets['Interest'] == 1])
uninterested = np.array(data_sets[data_sets['Interest'] == 0])

# print(int(len(interested)/(fs*interval))*fs*interval)
# print(int(len(interested)/(fs*interval))) #53
# print(int(len(uninterested)/(fs*interval))) #41

# interestedN = np.array(np.array_split(interested[:int(len(interested)/(fs*interval))*fs*interval], int((len(interested)/(fs*interval))), axis=0))
interestedN1 = np.array(np.array_split(np.array(np.array_split(interested[:int(len(interested)/(fs*interval))*fs*interval], int((len(interested)/(fs*interval))), axis=0)), k, axis=1)).reshape(10*-1, 512, 6)

# print(interestedN1.shape)

new_pos_segments = []
for n in range(500):
    ind = [interestedN1[randint(0, len(interestedN1)-1)] for x in range(10)]
    new_pos_segments.append(np.concatenate(ind, axis=0))

new_pos_segments = np.array(new_pos_segments)

uninterestedN1 = np.array(np.array_split(np.array(np.array_split(uninterested[:int(len(uninterested)/(fs*interval))*fs*interval], int((len(uninterested)/(fs*interval))), axis=0)), k, axis=1)).reshape(10*-1, 512, 6)

# print(uninterestedN1.shape)

new_neg_segments = []
for n in range(500):
    ind = [uninterestedN1[randint(0, len(uninterestedN1)-1)] for x in range(10)]
    new_neg_segments.append(np.concatenate(ind, axis=0))

new_neg_segments = np.array(new_neg_segments)

augmented_batches = np.concatenate((new_neg_segments, new_pos_segments), axis=0).reshape(-1*5120, 6, order='F')

# print(augmented_batches[:, 1:5].shape)

labels = np.concatenate((np.zeros(500), np.full(500, 1)))
# print(labels.shape)

features = PSD(augmented_batches[:, 1:5], fs, filtering=True)

# print(features)

normalized = descriptive_stats(features)

search = random_search_svm(normalized, labels)
print(search.best_params_)

