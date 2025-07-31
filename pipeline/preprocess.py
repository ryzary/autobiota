import pandas as pd
import numpy as np
import os
import re

def preprocess_data(file_path: str) -> str:
    """
    Intelligent preprocessing that automatically detects data format, orientation, and merges metadata
    """
    # Clean the file path - remove any extra text that might be included
    file_path = file_path.strip().strip("'\"")
    
    # Handle cases where LLM includes parameter names like "path="
    if 'path=' in file_path:
        file_path = file_path.split('path=')[-1].strip()
    
    # Handle cases where LLM includes extra text in the parameter
    if '\n' in file_path:
        file_path = file_path.split('\n')[0].strip()
    
    # Remove any trailing text after the file extension
    import re
    file_path = re.sub(r'(\.csv|\.tsv|\.txt).*', r'\1', file_path)
    
    # Final cleanup - remove any remaining quotes or spaces
    file_path = file_path.strip().strip("'\"")
    
    print(f"Processing file: {file_path}")
    
    # Skip processing if this is a metadata file
    if 'metadata' in file_path.lower():
        return f"Skipping metadata file: {file_path}. Metadata files are used for label extraction only."
    
    df = pd.read_csv(file_path)
    
    print(f"Original data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Look for metadata files in the same directory
    metadata_df = None
    base_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Common metadata file patterns
    metadata_patterns = [
        f"{base_name}_metadata",
        f"{base_name.replace('_', '')}_metadata", 
        "metadata",
        f"{base_name}_labels",
        f"{base_name}_clinical",
        f"{base_name}_phenotype"
    ]
    
    # Common file extensions for metadata
    metadata_extensions = ['.csv', '.tsv', '.txt', '.numbers']
    
    for pattern in metadata_patterns:
        for ext in metadata_extensions:
            metadata_path = os.path.join(base_dir, pattern + ext)
            if os.path.exists(metadata_path):
                try:
                    print(f"Found metadata file: {metadata_path}")
                    if ext == '.numbers':
                        # Handle Numbers files - try to read as CSV first
                        try:
                            metadata_df = pd.read_csv(metadata_path)
                        except:
                            print(f"Could not read {metadata_path} as CSV. Please convert to CSV format.")
                            continue
                    else:
                        # Handle CSV/TSV files
                        separator = '\t' if ext == '.tsv' else ','
                        metadata_df = pd.read_csv(metadata_path, sep=separator)
                    
                    print(f"Metadata shape: {metadata_df.shape}")
                    print(f"Metadata columns: {list(metadata_df.columns)}")
                    break
                except Exception as e:
                    print(f"Error reading metadata file {metadata_path}: {e}")
                    continue
        if metadata_df is not None:
            break
    
    # Detect sample ID column (various possible names)
    sample_id_patterns = ['sample_id', 'sampleid', 'sample', 'id', 'subject_id', 'patient_id']
    sample_id_col = None
    for pattern in sample_id_patterns:
        matching_cols = [col for col in df.columns if pattern.lower() in col.lower()]
        if matching_cols:
            sample_id_col = matching_cols[0]
            break
    
    # Detect label/target column (various possible names)
    label_patterns = ['label', 'class', 'target', 'diagnosis', 'disease', 'condition', 'status', 'group']
    label_col = None
    for pattern in label_patterns:
        matching_cols = [col for col in df.columns if pattern.lower() in col.lower()]
        if matching_cols:
            label_col = matching_cols[0]
            break
    
    # Detect if data needs to be transposed (samples in columns vs rows)
    # Heuristic: if we have many more columns than rows, samples might be in columns
    needs_transpose = False
    
    # Check if first column looks like taxonomic names (contains bacterial names)
    bacterial_indicators = ['bacteroides', 'clostridium', 'escherichia', 'lactobacillus', 
                          'bifidobacterium', 'prevotella', 'faecalibacterium', 'akkermansia']
    
    if df.shape[1] > df.shape[0] * 2:  # Many more columns than rows
        # Check if first column contains bacterial names
        first_col_text = str(df.iloc[:, 0].values).lower()
        if any(indicator in first_col_text for indicator in bacterial_indicators):
            needs_transpose = True
            print("Detected: Samples appear to be in columns, transposing data")
    
    if needs_transpose:
        # Transpose the data
        df = df.set_index(df.columns[0]).T
        df.index.name = 'sample_id'
        df = df.reset_index()
        
        # Re-detect columns after transpose
        sample_id_col = 'sample_id'
        # Label column might be in the data now, re-detect
        for pattern in label_patterns:
            matching_cols = [col for col in df.columns if pattern.lower() in col.lower()]
            if matching_cols:
                label_col = matching_cols[0]
                break
    
    # If no sample_id column found, create one
    if sample_id_col is None:
        df.insert(0, 'sample_id', [f'Sample_{i+1}' for i in range(len(df))])
        sample_id_col = 'sample_id'
        print("Created sample_id column")
    
    # Process metadata file if found
    if metadata_df is not None:
        print("Processing metadata file...")
        
        # Detect sample ID column in metadata (enhanced patterns)
        metadata_sample_col = None
        enhanced_sample_patterns = sample_id_patterns + ['sample id', 'sampleid', 'sample_id']
        for pattern in enhanced_sample_patterns:
            matching_cols = [col for col in metadata_df.columns if pattern.lower().replace('_', ' ') in col.lower() or pattern.lower().replace(' ', '_') in col.lower()]
            if matching_cols:
                metadata_sample_col = matching_cols[0]
                print(f"Found sample ID column in metadata: {metadata_sample_col}")
                break
        
        # If no sample ID found in metadata, use first column or index
        if metadata_sample_col is None:
            if len(metadata_df.columns) > 0:
                metadata_sample_col = metadata_df.columns[0]
                print(f"Using first column as sample ID in metadata: {metadata_sample_col}")
            else:
                print("Warning: Could not identify sample ID column in metadata")
        
        # Detect label column in metadata (enhanced patterns)
        metadata_label_col = None
        enhanced_label_patterns = label_patterns + ['group']
        for pattern in enhanced_label_patterns:
            matching_cols = [col for col in metadata_df.columns if pattern.lower() == col.lower()]
            if matching_cols:
                metadata_label_col = matching_cols[0]
                print(f"Found label column in metadata: {metadata_label_col}")
                break
        
        # If no exact match, try partial matching
        if metadata_label_col is None:
            for pattern in enhanced_label_patterns:
                matching_cols = [col for col in metadata_df.columns if pattern.lower() in col.lower()]
                if matching_cols:
                    metadata_label_col = matching_cols[0]
                    print(f"Found label column in metadata (partial match): {metadata_label_col}")
                    break
        
        # If no explicit label column, look for categorical columns that could be labels
        if metadata_label_col is None:
            for col in metadata_df.columns:
                if col != metadata_sample_col:
                    unique_vals = metadata_df[col].dropna().unique()
                    if len(unique_vals) <= 10 and len(unique_vals) >= 2:  # Reasonable number of categories
                        metadata_label_col = col
                        print(f"Inferred label column from metadata: {metadata_label_col}")
                        break
        
        # Merge metadata with main data
        if metadata_sample_col and metadata_label_col:
            # Prepare metadata for merging
            metadata_subset = metadata_df[[metadata_sample_col, metadata_label_col]].copy()
            metadata_subset.columns = ['merge_key', 'label_from_metadata']
            
            # Prepare main data for merging
            df_with_merge_key = df.copy()
            df_with_merge_key['merge_key'] = df_with_merge_key[sample_id_col]
            
            # Try different merge strategies
            merged = None
            
            # Strategy 1: Direct merge
            try:
                merged = df_with_merge_key.merge(metadata_subset, on='merge_key', how='left')
                if merged['label_from_metadata'].notna().sum() > 0:
                    print(f"Successfully merged {merged['label_from_metadata'].notna().sum()} labels via direct merge")
                else:
                    merged = None
            except:
                pass
            
            # Strategy 2: Try partial string matching if direct merge fails
            if merged is None or merged['label_from_metadata'].notna().sum() == 0:
                print("Trying partial string matching for sample IDs...")
                for idx, main_id in enumerate(df_with_merge_key['merge_key']):
                    if pd.isna(main_id):
                        continue
                    main_id_str = str(main_id).lower()
                    
                    for meta_idx, meta_id in enumerate(metadata_subset['merge_key']):
                        if pd.isna(meta_id):
                            continue
                        meta_id_str = str(meta_id).lower()
                        
                        # Check if one ID contains the other
                        if main_id_str in meta_id_str or meta_id_str in main_id_str:
                            if merged is None:
                                merged = df_with_merge_key.copy()
                                merged['label_from_metadata'] = None
                            merged.loc[idx, 'label_from_metadata'] = metadata_subset.loc[meta_idx, 'label_from_metadata']
                
                if merged is not None and merged['label_from_metadata'].notna().sum() > 0:
                    print(f"Successfully merged {merged['label_from_metadata'].notna().sum()} labels via partial matching")
            
            # Use merged labels if successful
            if merged is not None and merged['label_from_metadata'].notna().sum() > 0:
                df = merged.drop(['merge_key'], axis=1)
                # Replace or add label column
                if label_col and label_col in df.columns:
                    df[label_col] = df['label_from_metadata'].fillna(df[label_col])
                else:
                    df['label'] = df['label_from_metadata']
                    label_col = 'label'
                df = df.drop(['label_from_metadata'], axis=1)
                print(f"Updated main data with labels from metadata")
            else:
                print("Warning: Could not successfully merge metadata labels")
    
    # If no label column found after metadata processing, try to infer from data or create dummy labels
    if label_col is None or label_col not in df.columns:
        # Look for binary patterns in data that might indicate labels
        for col in df.columns:
            if col != sample_id_col and df[col].dtype == 'object':
                unique_vals = df[col].unique()
                if len(unique_vals) <= 10:  # Reasonable number of categories
                    label_col = col
                    print(f"Inferred label column: {label_col}")
                    break
        
        # If still no label found, create dummy labels
        if label_col is None or label_col not in df.columns:
            df['label'] = 'unknown'
            label_col = 'label'
            print("Created dummy label column")
    
    # Identify metadata columns
    metadata_cols = [sample_id_col, label_col]
    
    # Identify abundance columns (numeric columns that aren't metadata)
    abundance_cols = []
    for col in df.columns:
        if col not in metadata_cols:
            # Try to convert to numeric, keep if successful
            try:
                pd.to_numeric(df[col], errors='raise')
                abundance_cols.append(col)
            except (ValueError, TypeError):
                # Skip non-numeric columns
                print(f"Skipping non-numeric column: {col}")
                continue
    
    if not abundance_cols:
        raise ValueError("No numeric abundance columns found in the data")
    
    print(f"Found {len(abundance_cols)} abundance columns")
    print(f"Sample ID column: {sample_id_col}")
    print(f"Label column: {label_col}")
    
    # Extract metadata and abundance data
    metadata = df[metadata_cols].copy()
    abundance = df[abundance_cols].copy()
    
    # Convert abundance columns to numeric
    for col in abundance_cols:
        abundance[col] = pd.to_numeric(abundance[col], errors='coerce')
    
    # Handle missing values
    abundance = abundance.fillna(0)
    
    # Normalize rows to relative abundance (each row sums to 1)
    row_sums = abundance.sum(axis=1)
    # Avoid division by zero
    row_sums = row_sums.replace(0, 1)
    normalized = abundance.div(row_sums, axis=0)
    
    # Combine metadata back with normalized values
    result = pd.concat([metadata, normalized], axis=1)
    
    # Save preprocessed data
    output_path = file_path.replace(".csv", "_preprocessed.csv")
    result.to_csv(output_path, index=False)
    
    print(f"Preprocessed data shape: {result.shape}")
    print(f"Sample of preprocessed data:")
    print(result.head())
    
    return f"Preprocessing complete. Detected {len(abundance_cols)} bacterial features. Saved to: {output_path}"
