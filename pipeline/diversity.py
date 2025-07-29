import pandas as pd
from scipy.stats import entropy

def compute_diversity(path: str) -> str:
    df = pd.read_csv(path)
    if "label" in df.columns:
        df = df.drop(columns=["label"])
    alpha = df.apply(entropy, axis=1)
    result_path = "output/diversity/diversity.csv"
    alpha.to_csv(result_path, index=False)
    return f"Alpha diversity computed and saved to {result_path}"