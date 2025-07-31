import pandas as pd
from scipy.stats import entropy
import os

def compute_diversity(path: str) -> str:
    df = pd.read_csv(path)
    if "label" in df.columns:
        df = df.drop(columns=["label"])
    if "sample_id" in df.columns:
        df = df.drop(columns=["sample_id"])
    
    # Ensure all columns are numeric
    df = df.select_dtypes(include=['number'])
    
    alpha = df.apply(entropy, axis=1)
    
    os.makedirs("outputs/diversity", exist_ok=True)
    result_path = "outputs/diversity/diversity.csv"
    alpha.to_csv(result_path, index=False)
    return f"Alpha diversity computed and saved to {result_path}"
