import pandas as pd


def extract_data(file_path):
    """
    Extract data from a CSV file.
    """

    try:
        df = pd.read_csv(file_path)

        print("✅ Data extracted successfully!")
        print(f"Total Records: {len(df)}")
        print(f"Total Columns: {len(df.columns)}")

        return df

    except FileNotFoundError:
        print("❌ File not found.")
        print("Check if the CSV exists at:", file_path)
        return None

    except Exception as e:
        print("❌ Error:", e)
        return None