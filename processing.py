import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from sklearn.cluster import KMeans
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes, AggOperations, WindowFunctions, NoiseTypes
from scipy.signal import butter, lfilter, lfilter_zi
from tqdm import tqdm 
from sklearn.preprocessing import StandardScaler

def PSD(df, fs, filtering=False, streaming=False):

    if streaming == True:
        index = len(df)
        feature_vectors = []
        if filtering == True:
            
            DataFilter.perform_bandpass(df[:], fs, 15.0, 6.0, 4,
                                FilterTypes.BESSEL.value, 0)
            DataFilter.remove_environmental_noise(df[:], fs, NoiseTypes.SIXTY.value)

        for y in range(0,index,fs):

            f, Pxx_den = signal.welch(df[y:y+fs], fs=fs, nfft=256) #simulated 4 point overlap
            # plt.semilogy(f, Pxx_den)
            # plt.ylim([0.5e-3, 1])
            # plt.xlabel('frequency [Hz]')
            # plt.ylabel('PSD [V**2/Hz]')
            # plt.show()

            ind_delta, = np.where(f < 4)
            meanDelta = np.mean(Pxx_den[ind_delta], axis=0)
            # Theta 4-8
            ind_theta, = np.where((f >= 4) & (f <= 8))
            meanTheta = np.mean(Pxx_den[ind_theta], axis=0)
            # Alpha 8-12
            ind_alpha, = np.where((f >= 8) & (f <= 12))
            meanAlpha = np.mean(Pxx_den[ind_alpha], axis=0)
            # Beta 12-30
            ind_beta, = np.where((f >= 12) & (f < 30))
            meanBeta = np.mean(Pxx_den[ind_beta], axis=0)
            # Gamma 30-100+
            ind_Gamma, = np.where((f >= 30) & (f < 40))
            meanGamma = np.mean(Pxx_den[ind_Gamma], axis=0)

            feature_vectors.insert(y, [meanDelta, meanTheta, meanAlpha, meanBeta, meanGamma])

        powers = np.log10(np.asarray(feature_vectors))

        powers = powers.reshape(5)
        return powers
    
    else:
        index, ch = df.shape[0], df.shape[1]
        feature_vectors = [[] for _ in range(ch)]

        for x in tqdm(range(ch)):

            if filtering == True:

                DataFilter.perform_bandpass(df[:, x], fs, 15.0, 6.0, 4,
                                    FilterTypes.BESSEL.value, 0)
                DataFilter.remove_environmental_noise(df[:, x], fs, NoiseTypes.SIXTY.value)

            for y in range(0,index,fs):

                f, Pxx_den = signal.welch(df[y:y+fs, x], fs=fs, nfft=256) #simulated 4 point overlap
                # plt.semilogy(f, Pxx_den)
                # plt.ylim([0.5e-3, 1])
                # plt.xlabel('frequency [Hz]')
                # plt.ylabel('PSD [V**2/Hz]')
                # plt.show()

                ind_delta, = np.where(f < 4)
                meanDelta = np.mean(Pxx_den[ind_delta], axis=0)
                # Theta 4-8
                ind_theta, = np.where((f >= 4) & (f <= 8))
                meanTheta = np.mean(Pxx_den[ind_theta], axis=0)
                # Alpha 8-12
                ind_alpha, = np.where((f >= 8) & (f <= 12))
                meanAlpha = np.mean(Pxx_den[ind_alpha], axis=0)
                # Beta 12-30
                ind_beta, = np.where((f >= 12) & (f < 30))
                meanBeta = np.mean(Pxx_den[ind_beta], axis=0)
                # Gamma 30-100+
                ind_Gamma, = np.where((f >= 30) & (f < 40))
                meanGamma = np.mean(Pxx_den[ind_Gamma], axis=0)
                # print(y)
                feature_vectors[x].insert(y, [meanTheta/meanAlpha, meanTheta/meanBeta, meanTheta/meanGamma, meanAlpha/meanBeta, meanAlpha/meanGamma, meanBeta/meanGamma])

        powers = np.log10(np.asarray(feature_vectors))

        # powers = powers.reshape(-1, 5*ch)
        return powers

def svm_model(data, labels):

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(rolling, labels, test_size = 0.20)

    from sklearn.svm import SVC
    svclassifier = SVC(kernel='rbf')
    svclassifier.fit(X_train, y_train)
    
    y_pred = svclassifier.predict(X_test)

    from sklearn.metrics import classification_report, confusion_matrix
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return svclassifier

window_size = 5
interval = 20
sample_rate = 256

filenames = ['avatar1', 'avengers1', 'bbc1', 'bear1', 'bighero1', 'creed1', 'edgeoftmr11', 'gunviolence1', 'ironman1', 'joe1', 'lex1', 'vox1']

files = [pd.read_csv(('{}.csvprocessed.csv').format(name)) for name in filenames]

data_sets = pd.concat(files, ignore_index=True).dropna()
labels = data_sets["Interest"]

# print(data_sets.head())

labels_norm = [1 if x == 4 or x == 5 else 0 for x in labels]

labels_fil = [labels_norm[x] for x in range(0, len(labels_norm), sample_rate*interval)][:94]

# print(len(labels_fil)) #95

data = data_sets.drop(["Interest"], axis=1).to_numpy()

# print(data.shape) #484352

features = PSD(data[:, 1:], sample_rate, filtering=True)
print(features.shape)

# features = features[:, :160, :].reshape(160, 4, 6)

ch, length, feats = features.shape[0], features.shape[1], features.shape[2] 
print(ch, length, feats)
rolling = [[[[] for _ in range(int(length/interval))] for _ in range(feats)] for _ in range(ch)] #(4, 6, 94)
print(np.array(rolling).shape)

for interv in range(int(length/interval)): #(+20)
    for channel in range(ch):
        for f in range(feats):
            window = pd.Series(features[channel, interv*interval:interv*interval+interval, f]).rolling(window_size).mean().dropna()
            rolling[channel][f][interv].append([window.min(), window.max(), window.skew(), window.median()])

rolling = np.array(rolling, dtype=object).reshape(94, ch*6*4) #(8, 4, 6, 4)
print(rolling.shape)
print(len(labels_fil))

scaler = StandardScaler()
print(scaler.fit_transform(rolling))

svmclassifier = svm_model(rolling, labels_fil)

