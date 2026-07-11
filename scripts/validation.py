def validate_data(df):
    """
    Validate the dataset before loading.
    """

    print("\n========== Data Validation ==========")

    # Missing Values
    print("\nMissing Values Per Column:")
    print(df.isnull().sum())

    # Total Missing Values
    print("\nTotal Missing Values:", df.isnull().sum().sum())

    # Duplicate Rows
    duplicate_rows = df.duplicated().sum()
    print("\nDuplicate Rows:", duplicate_rows)

    # Fraud Distribution
    print("\nFraud Distribution:")
    print(df["isFraud"].value_counts())

    # Transaction Type Distribution
    print("\nTransaction Types:")
    print(df["type"].value_counts())

    print("\n✅ Validation Completed!")

    return df