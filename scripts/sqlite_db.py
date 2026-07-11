import sqlite3


def load_to_sqlite(csv_path):

    print("\n========== SQLite Loading ==========")

    import pandas as pd

    df = pd.read_csv(csv_path)

    conn = sqlite3.connect("finflow.db")

    df.to_sql(
        "transactions",
        conn,
        if_exists="replace",
        index=False
    )

    print("✅ Data Loaded into SQLite!")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    total = cursor.fetchone()[0]

    print(f"Rows in Database : {total}")

    conn.close()