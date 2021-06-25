import pandas as pd  
import numpy as np

filenames = ['avatar1', 'avengers1', 'bbc1', 'bear1', 'bighero1', 'creed1', 'edgeoftmr11', 'gunviolence1', 'ironman1', 'joe1', 'lex1', 'vox1']

files = [pd.read_csv(('datasets/{}.csvprocessed.csv').format(name))['Interest'] for name in filenames]

labels = pd.concat(files, ignore_index=True).dropna()

percentile = np.percentile(labels, 80)

labels_norm = [1 if x == 4 or x == 5 else 0 for x in labels]

# print(labels_norm)

