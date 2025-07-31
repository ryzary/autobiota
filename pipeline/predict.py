import pandas as pd
import joblib

def predict_from_model(path: str) -> str:
    df = pd.read_csv(path)
    if "sample_id" in df.columns:
        df = df.drop(columns=["sample_id"])
    model = joblib.load("outputs/model/disease_classifier.joblib")
    pred = model.predict(df)
    return f"Prediction: {pred[0]}"
