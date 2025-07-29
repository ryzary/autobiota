import pandas as pd
import joblib
from sklearn.metrics import classification_report


def evaluate_model(eval_csv_path: str) -> str:
    # Load evaluation dataset CSV
    # Strip quotes if present
    eval_csv_path = eval_csv_path.strip().strip("'\"")
    df = pd.read_csv(eval_csv_path)

    # Load model file separately
    model = joblib.load("model/disease_classifier.joblib")

    # Prepare features and target
    X_eval = df.drop(columns=["label", "sample_id"])
    y_true = df["label"]

    # Predict and evaluate
    y_pred = model.predict(X_eval)
    report = classification_report(y_true, y_pred)
    with open("outputs/eval/evaluation.txt", "w") as f:
        f.write(report)
    return f"Model evaluation saved to outputs/eval/evaluation.txt\n{report}"