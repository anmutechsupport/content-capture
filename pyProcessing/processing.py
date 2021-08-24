import math
import pandas as pd
import numpy as np
from scipy import signal
from brainflow.data_filter import DataFilter, FilterTypes, NoiseTypes
from tqdm import tqdm 
from sklearn.preprocessing import StandardScaler
from scipy.special import logsumexp

def PSD(df, fs, filtering=False):

    print(df.shape)
    index, ch = df.shape[0], df.shape[1]
    feature_vectors = [[] for _ in range(ch)]

    for x in tqdm(range(ch)):

        if filtering == True:

            DataFilter.perform_bandpass(df[:, x], fs, 12.6491106, 36.0, 4,
                                FilterTypes.BESSEL.value, 0)
            DataFilter.remove_environmental_noise(df[:, x], fs, NoiseTypes.SIXTY.value)

        for y in range(0,index,fs):
            
            if len(df[y:y+fs, x]) != 256:
                break

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
    return powers

def log_PSD(df, fs, filtering=False):

    print(df.shape)
    index, ch = df.shape[0], df.shape[1]
    feature_vectors = [[] for _ in range(ch)]

    for x in tqdm(range(ch)):

        if filtering == True:

            DataFilter.perform_bandpass(df[:, x], fs, 15.0, 6.0, 4,
                                FilterTypes.BESSEL.value, 0)
            DataFilter.remove_environmental_noise(df[:, x], fs, NoiseTypes.SIXTY.value)

        for y in range(0,index,fs):
            
            if len(df[y:y+fs, x]) != 256:
                break

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
            # feature_vectors[x].insert(y, [np.exp(logsumexp(meanTheta) - logsumexp(meanAlpha)), np.exp(logsumexp(meanTheta) - logsumexp(meanBeta)), np.exp(logsumexp(meanTheta) - logsumexp(meanGamma)), np.exp(logsumexp(meanAlpha) - logsumexp(meanBeta)), np.exp(logsumexp(meanAlpha) - logsumexp(meanGamma)), np.exp(logsumexp(meanBeta) - logsumexp(meanGamma))])
            feature_vectors[x].insert(y, [np.exp(logsumexp(meanTheta) - logsumexp(meanAlpha)), np.exp(logsumexp(meanTheta) - logsumexp(meanBeta)), np.exp(logsumexp(meanTheta) - logsumexp(meanGamma)), np.exp(logsumexp(meanAlpha) - logsumexp(meanBeta)), np.exp(logsumexp(meanAlpha) - logsumexp(meanGamma)), np.exp(logsumexp(meanBeta) - logsumexp(meanGamma))])

    # powers = np.log10(np.asarray(feature_vectors))
    powers = np.asarray(feature_vectors)
    return powers

def svm_model(data, labels):

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.1)

    from sklearn.svm import SVC
    svclassifier = SVC(kernel='rbf', class_weight='balanced', C=1, gamma=0.001)
    svclassifier.fit(X_train, y_train)
    
    y_pred = svclassifier.predict(X_test)

    from sklearn.metrics import classification_report, confusion_matrix
    print("SVM")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # from sklearn.model_selection import cross_val_score
    # scores = cross_val_score(svclassifier, data, labels, cv=10)
    # print(scores)

    return svclassifier

def random_search_svm(data, labels):

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.1)

    from sklearn.model_selection import GridSearchCV 
    from sklearn.model_selection import train_test_split
    from sklearn.svm import SVC 

    parameters = {'C': [0.001, 0.01, 0.1, 1, 10, 100], 
                'gamma': [0.001, 0.01, 0.1, 1, 10, 100]}

    search = GridSearchCV(SVC(), parameters, cv=5)
    
    results  = search.fit(X_train, y_train)

    return results


def tree_model(data, labels):

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.1)

    from sklearn.tree import DecisionTreeClassifier

    treeclassifier = DecisionTreeClassifier(criterion='gini', max_features='log2', min_samples_leaf=1, min_samples_split=2, max_depth=5)
    treeclassifier.fit(X_train, y_train)
    
    y_pred = treeclassifier.predict(X_test)

    from sklearn.metrics import classification_report, confusion_matrix
    print("Decision Tree")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return treeclassifier

def gaussian_nb(data, labels):

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.1)
    
    from sklearn.naive_bayes import GaussianNB

    clf = GaussianNB()
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)

    from sklearn.metrics import classification_report, confusion_matrix
    print("Naive Bayes")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return clf

def logreg_model(data, labels):

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.1)

    from sklearn.linear_model import LogisticRegression
    logregclassifier = LogisticRegression(C=0.001)
    logregclassifier.fit(X_train, y_train)
    
    y_pred = logregclassifier.predict(X_test)

    from sklearn.metrics import classification_report, confusion_matrix
    print("Logistic Regression")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return logregclassifier

def random_forest(data, labels):

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.1)

    from sklearn.ensemble import RandomForestClassifier
    randomforest = RandomForestClassifier(criterion='gini', max_features='log2', min_samples_leaf=3,  min_samples_split=2, max_depth=5, n_estimators=5)
    randomforest.fit(X_train, y_train)
    
    y_pred = randomforest.predict(X_test)

    from sklearn.metrics import classification_report, confusion_matrix
    print("Random Forests")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return randomforest

def ada_boost(data, labels):

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.1)
    
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import AdaBoostClassifier
    adaboost = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(criterion='gini', max_features='log2', min_samples_leaf=1, min_samples_split=2, max_depth=5), learning_rate=0.02, n_estimators=5)
    adaboost.fit(X_train, y_train)
    
    y_pred = adaboost.predict(X_test)

    from sklearn.metrics import classification_report, confusion_matrix
    print("Ada_Boost")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return adaboost

def descriptive_stats(features):
    window_size = 5
    interval = 20

    ch, length, feats = features.shape[0], features.shape[1], features.shape[2] 
    # print(ch, length, feats)
    rolling = [[[[] for _ in range(math.floor(length/interval))] for _ in range(feats)] for _ in range(ch)] #(4, 6, 94)
    # print(np.array(rolling).shape)

    for interv in tqdm(range(int(length/interval))): #(+20)
        for channel in range(ch):
            for f in range(feats):
                window = pd.Series(features[channel, interv*interval:interv*interval+interval, f]).rolling(window_size).mean().dropna()
                rolling[channel][f][interv].append([window.min(), window.max(), window.skew(), window.median()])

    rolling = np.array(rolling, dtype=object).reshape(-1, ch*6*4)
    
    scaler = StandardScaler()
    normalized = scaler.fit_transform(rolling)

    return normalized


def create_modelFinal():
    fs = 256
    interval = 20

    filenames = ['avatar1', 'avengers1', 'bbc1', 'bear1', 'bighero1', 'creed1', 'edgeoftmr11', 'gunviolence1', 'ironman1', 'joe1', 'lex1', 'vox1']
    files = [pd.read_csv(('datasets/{}.csvprocessed.csv').format(name)) for name in filenames]

    data_sets = pd.concat(files, ignore_index=True).dropna()
    labels = data_sets["Interest"]
     
    labels_norm = [1 if x == 4 or x == 5 else 0 for x in labels]

    labels_fil = [labels_norm[x] for x in range(0, len(labels_norm), fs*interval)][:94]

    # print(len(labels_fil)) #95

    data = data_sets.drop(["Interest"], axis=1).to_numpy()

    # print(data[:, 1:].shape) #(484352, 4)

    features = PSD(data[:, 1:], fs, filtering=True)
    # print(features.shape)

    # features = features[:, :160, :].reshape(160, 4, 6)

    normalized = descriptive_stats(features)
    # print(rolling.shape)
    # print(np.count_nonzero(np.array(labels_fil) == 1))

    # print(normalized.shape)

    naivebayes = gaussian_nb(normalized, labels_fil)
    # logregclassifier = logreg_model(normalized, labels_fil)
    # dectreeclassifier = tree_model(normalized, labels_fil)
    # randomforestclassifier = random_forest(normalized, labels_fil)
    # adaboostclassifier = ada_boost(normalized, labels_fil)

    return naivebayes 

# create_modelFinal()

#Data augmentation + transfer learning
#add audio using ffmpeg
