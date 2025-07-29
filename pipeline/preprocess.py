import pandas as pd
import os

def preprocess_data(file_path: str) -> str:
    # Strip quotes if present
    file_path = file_path.strip().strip("'\"")
    df = pd.read_csv(file_path)

    # Keep metadata
    metadata_cols = ['sample_id', 'label']
    metadata = df[metadata_cols]

    # Select only numeric abundance columns
    abundance = df.drop(columns=metadata_cols)

    # Normalize rows to relative abundance
    normalized = abundance.div(abundance.sum(axis=1), axis=0)

    # Combine metadata back with normalized values
    result = pd.concat([metadata, normalized], axis=1)

    # Save preprocessed data (optional)
    output_path = file_path.replace(".csv", "_preprocessed.csv")
    result.to_csv(output_path, index=False)

    return f"Preprocessing complete. Saved to: {output_path}"