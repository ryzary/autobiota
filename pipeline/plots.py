import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import os

def plot_results(path: str) -> str:
    df = pd.read_csv(path)

    if "label" in df.columns:
        labels = df["label"]
        df = df.drop(columns=["label"])
    else:
        labels = ["unknown"] * len(df)

    # Only keep numeric columns
    df = df.select_dtypes(include=["number"])

    pca = PCA(n_components=2)
    components = pca.fit_transform(df)

    plt.figure(figsize=(6, 5))
    for l in set(labels):
        idx = [i for i, val in enumerate(labels) if val == l]
        plt.scatter(components[idx, 0], components[idx, 1], label=l)

    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA of Microbiome Data")
    plt.legend()

    os.makedirs("outputs/plots", exist_ok=True)
    plot_path = "outputs/plots/pca_plot.png"
    plt.savefig(plot_path)
    plt.close()

    return f"PCA plot saved to {plot_path}"
