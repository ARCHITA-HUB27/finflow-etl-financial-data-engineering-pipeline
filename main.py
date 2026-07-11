from scripts.extract import extract_data
from scripts.transform import clean_data
from scripts.validation import validate_data
from scripts.load import save_processed_data
from scripts.spark_processing import process_data_with_spark
from scripts.sqlite_db import load_to_sqlite


def main():

    raw_file = "data/raw/transactions.csv"
    processed_file = "data/processed/cleaned_transactions.csv"

    print("=" * 60)
    print("      FinFlow ETL Data Engineering Pipeline")
    print("=" * 60)

    # ---------------- Extract ----------------
    print("\nSTEP 1 : Extract")
    df = extract_data(raw_file)

    # ---------------- Transform ----------------
    print("\nSTEP 2 : Transform")
    cleaned_df = clean_data(df)

    # ---------------- Validation ----------------
    print("\nSTEP 3 : Validation")
    validated_df = validate_data(cleaned_df)

    # ---------------- Load CSV ----------------
    print("\nSTEP 4 : Save Processed CSV")
    save_processed_data(validated_df, processed_file)

    # ---------------- SQLite ----------------
    print("\nSTEP 5 : SQLite")
    load_to_sqlite(processed_file)

    # ---------------- PySpark ----------------
    print("\nSTEP 6 : PySpark")
    process_data_with_spark(processed_file)

    print("\n")
    print("=" * 60)
    print("🎉 FinFlow ETL Pipeline Completed Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()