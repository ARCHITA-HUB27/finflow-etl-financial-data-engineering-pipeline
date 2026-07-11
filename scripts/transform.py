import pandas as pd


def clean_data(df):
    """
    Clean the transaction dataset.
    """

    print("\n========== Data Cleaning ==========")

    # Remove duplicate rows
    duplicate_count = df.duplicated().sum()
    df = df.drop_duplicates()

    # Remove missing values
    missing_before = df.isnull().sum().sum()
    df = df.dropna()

    # Reset index
    df.reset_index(drop=True, inplace=True)

    print(f"Duplicates Removed: {duplicate_count}")
    print(f"Missing Values Removed: {missing_before}")
    print("✅ Cleaning Completed!")

    return df