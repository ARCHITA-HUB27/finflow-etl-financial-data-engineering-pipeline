import os


def save_processed_data(df, output_path):
    """
    Save the cleaned dataset to a CSV file.
    """

    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

  
    df.to_csv(output_path, index=False)

    print("\n========== Data Load ==========")
    print("✅ Processed dataset saved successfully!")
    print(f"Location: {output_path}")