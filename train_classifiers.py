from scipy.io import arff
import pandas as pd
from sklearn.model_selection import train_test_split


def train_model(infile):
    with open(infile) as f:
        data, meta = arff.loadarff(f)
    df = pd.DataFrame(data)
    df.dropna(1, inplace=True)
    y_accent = df['accent'].str.decode('utf-8')
    X_accent = df.iloc[:, :-3]  # choose all columns without annotated data
    df['accent'] = y_accent
    # select only accented syllables
    df_tone = df.loc[df['accent'] == 'accented']
    y_tone = df_tone['tone'].str.decode('utf-8')
    X_tone = df_tone.iloc[:, :-3]
    # split datasets into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_tone, y_tone)
    # Random Forest Classifier:
    # 0.87 precision / 0.7 recall for accent detection (can use n_estimators=20)
    # ~0.7 accuracy for accent classification
