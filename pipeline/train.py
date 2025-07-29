import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
    
def train_model(path: str) -> str:
    df = pd.read_csv(path)
    X = df.drop(columns=["label","sample_id"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, "model/disease_classifier.joblib")
    return "Model trained and saved to model/disease_classifier.joblib"