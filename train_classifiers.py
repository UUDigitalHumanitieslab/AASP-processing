from scipy.io import arff
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split


def train_model(infile):
    with open(infile) as f:
        data, meta = arff.loadarff(f)
    df = pd.DataFrame(data)
    df.dropna(1, inplace=True)
    y_accent = df['accent'].str.decode('utf-8')
    X_accent = df.iloc[:, :-3]  # choose all columns without annotated data
    X_train, X_test, y_train, y_test = train_test_split(X_accent, y_accent)
    accent_classifier = RandomForestClassifier(n_estimators=20)
    accent_classifier.fit(X_train, y_train)
    y_predicted = accent_classifier.predict(X_test)
    precision = precision_score(y_test, y_predicted)
    recall = recall_score(y_test, y_predicted)
    print(f"Precision of accent classifier: {precision}")
    print(f"Recall of accent classifier: {recall}")
    df['accent'] = y_accent
    # select only accented syllables
    df_tone = df.loc[df['accent'] == 'accented']
    y_tone = df_tone['tone'].str.decode('utf-8')
    X_tone = df_tone.iloc[:, :-3]
    # split datasets into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_tone, y_tone)
    tone_classifier = RandomForestClassifier(n_estimators=20)
    tone_classifier.fit(X_train, y_train)
    y_predicted = tone_classifier.predict(X_test)
    precision = precision_score(y_test, y_predicted)
    recall = recall_score(y_test, y_predicted)
    print(f"Precision of tone classifier: {precision}")
    print(f"Recall of tone classifier: {recall}")

    # Random Forest Classifier:
    # 0.87 precision / 0.7 recall for accent detection (can use n_estimators=20)
    # ~0.7 accuracy for accent classification
